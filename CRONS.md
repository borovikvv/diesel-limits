# Cron Jobs — Diesel Limits

Two **Hermes Agent** cron jobs run daily on the server to collect fuel price data and publish updates to the map and Telegram channel.

- **Hermes** is an LLM-driven agent framework. Each cron job gives the agent a prompt with steps; the agent executes tools (web search, file ops, SQL queries, scripts) autonomously.
- Database: SQLite at `/root/diesel_limits/restrictions.db`
- Web root: `/srv/static/` (served by Caddy at cockpit.borovikvv.ru/static/)

---

## 1. diesel-heatmap-daily — 02:00 MSK

Collects fresh prices and restrictions. Runs the full ingestion pipeline.

| Field | Value |
|---|---|
| **Job ID** | `c20d0ade1f2f` |
| **LLM model** | deepseek-v4-flash via opencode-go |
| **Hermes toolsets** | `web`, `terminal`, `file` |
| **Workdir** | not set (runs from Hermes home) |

### Steps

**Step 1: Price scraping via web_extract**

Extracts prices from two sources:

- `https://www.sravni.ru/dtp/tpost/i2d0xhezg1-tseni-na-dizel-v-rossii`
- `https://driff.ru/ceny-na-dizel-v-rossii/`

Extracts pairs **(region, price in ₽/L)** for all Russian regions listed.

**Step 2: Generate heatmap**

```bash
python3 /root/diesel_limits/gen_diesel_map.py
cp /root/diesel_limits/tmp/diesel_heatmap.png /srv/static/diesel.png
```

**Step 3: Search for restrictions via web_search (LLM-driven)**

The agent runs 8+ web searches to find new fuel restriction data:

1. `"ограничения на продажу дизельного топлива АЗС регионы 2026"`
2. `"лимиты заправки дизеля физические лица РФ июль 2026"`
3. `"АЗС лимиты дизель регионы города"`
4. `"ограничения на дизель для юридических лиц топливные карты"`
5. `"дефицит дизельного топлива ограничения 2026"`
6. `"топливные карты ограничения лимиты дизель 2026"`
7. `"дизель грузовики ограничения заправка регионы 2026"`
8. `"ограничения продажа дизеля дизельное топливо лимиты июль 2026"`

Plus news site–specific searches:
- `site:lenta.ru дизель ограничения лимиты 2026`
- `site:rbc.ru дизель ограничения лимиты 2026`

(web_search is a built-in Hermes tool — no API keys or tokens are stored in the job definition.)

**Step 4: Extract and persist restriction records**

For each source found, the agent extracts:
- **region**, **city** (if present), **network** (fuel station brand)
- **client_type**: `физлица`, `юридические лица`, or `все`
- **limit_type**: volume / amount / prohibition / time
- **limit_value**: e.g. `"50 л"`, `"только в бак"`
- **source_url**, **source_date**

Insert into SQLite with change tracking:

```python
# Pseudocode — equivalent Python is embedded in the cron prompt
cur = db.execute('''
    SELECT id, limit_value FROM restrictions
    WHERE region=? AND COALESCE(network,'')=COALESCE(?,'')
      AND client_type=? AND limit_type=? AND is_current=1
''', (region, net or '', client, limit_type)).fetchone()

if cur and cur[1] != value:
    # Mark old record as not current
    db.execute('UPDATE restrictions SET is_current=0, previous_value=limit_value WHERE id=?', (cur[0],))

if not cur or cur[1] != value:
    # Insert new record
    db.execute('''
        INSERT OR IGNORE INTO restrictions
        (region, network, client_type, limit_type, limit_value, source_url, source_date)
        VALUES (?,?,?,?,?,?,?)
    ''', (region, net, client, limit_type, value, url, date))
```

This ensures that if a limit changes (e.g. from `"50 л"` to `"30 л"`), the old value is preserved as `previous_value` and the new one becomes `is_current=1`.

**Step 5: Save prices**

For each price found in Step 1:

```python
db.execute('''
    INSERT OR REPLACE INTO prices
    (region, price, source_url, source_date, updated_at)
    VALUES (?,?,?,?, datetime('now'))
''', (region, price_rub, source_url, source_date))
```

**Step 6: Regenerate site data**

```bash
python3 /root/diesel_limits/dump_data_json.py
python3 /root/diesel_limits/dump_history.py
```

`dump_data_json.py` reads the SQLite DB → produces `/srv/static/data.json` (with `price_spark` per region for sparklines) and copies `index.html` from the repo.

`dump_history.py` writes `/srv/static/history/<region>.json` for each region — price history (90 days) and limit change timeline, lazy-loaded by the region card.

**Step 7: Verify**

Reports counts back: prices, active restrictions, total restrictions, number of changes.

---

## 2. publish-diesel-daily — 11:00 MSK

Generates a human-readable summary of the day's changes and publishes to Telegram.

| Field | Value |
|---|---|
| **Job ID** | `5792c3b0a0b0` |
| **LLM model** | deepseek-v4-flash via opencode-go |
| **Hermes toolsets** | `terminal`, `file` (no web access) |
| **Workdir** | not set |

### Steps

**Step 1: Ensure map image exists**

If `/srv/static/diesel.png` is older than 24 hours, regenerate:

```bash
python3 /root/diesel_limits/gen_diesel_map.py
cp /root/diesel_limits/tmp/diesel_heatmap.png /srv/static/diesel.png
```

**Step 2: Query changes from SQLite** (not status — only deltas)

Runs SQL queries on `/root/diesel_limits/restrictions.db` for the last 24 hours:
- Changed records: `previous_value IS NOT NULL AND updated_at >= datetime('now', '-1 day')`
- New records: `previous_value IS NULL AND updated_at >= datetime('now', '-1 day')`  
- Updated prices: `prices.updated_at >= datetime('now', '-1 day')`

**If zero changes** → only the map is published. Summary and changelog file are skipped.

**Step 3: Publish map to Telegram** (always, every day)

- **Map image**: sent via curl using `TG_BOT_TOKEN_DIESEL` environment variable to chat `@disel_limits_update` (chat ID `-1004299364641`)

**Step 4: Publish summary** (only if changes exist)

- **Summary text**: sent as a separate message in Russian. Describes what changed — new limits, removed limits, price changes. Not a full status report.

**Step 5: Save summary for the site** (only if changes exist)

Writes the same summary text to `/srv/static/changelog_latest.txt`:

```
Первая строка — текст summary
Вторая строка — дата (например 07.07.2026 11:00)
```

The site reads this file to show the latest update description. (No DB query, no Telegram API — just a file.)

---

## How to modify

These cron jobs are defined inside Hermes Agent's scheduler. To change prompt or schedule, edit the job via Telegram chat with Hermes or use the `cronjob` tool in a Hermes session.

### Design principles

- **No Firecrawl/api keys in the repo.** Token `TG_BOT_TOKEN_DIESEL` is set in OS environment variables, referenced as `$TG_BOT_TOKEN_DIESEL`. web_search/web_extract are built-in Hermes tools.
- **Git repo is source of truth.** Scripts (`dump_data_json.py`, `gen_diesel_map.py`, DB schema) live in this repo. Cron prompts reference them by absolute path.
- **File-based changelog.** The site reads `changelog_latest.txt` — no database queries for the summary.
- **Data flow**: web → SQLite (`restrictions.db`) → `dump_data_json.py` → `data.json` → frontend.
