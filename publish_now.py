#!/usr/bin/env python3
"""publish_now.py — публикация карты + summary в @disel_limits_update.

Контракт:
- Карта /srv/static/diesel.png: если старше 24ч -> gen_diesel_map.py + copy
- Summary только если за 24ч есть дельты (изменения/новые/цены)
- Токен: TG_BOT_TOKEN_DIESEL из env
- Chat: -1004299364641 (@disel_limits_update)
- Вся публичная текстовка — строго кириллицей (русский)
- HTTP 408 от Telegram API не означает недоставку (память проекта)
"""
import os, sys, time, sqlite3, subprocess, requests, shutil
from datetime import datetime, timezone, timedelta
from PIL import Image

DB = "/root/diesel_limits/restrictions.db"
MAP_PATH = "/srv/static/diesel.png"
MAP_SRC = "/root/diesel_limits/tmp/diesel_heatmap.png"
GEN_SCRIPT = "/root/diesel_limits/gen_diesel_map.py"
CHANGELOG = "/srv/static/changelog_latest.txt"
CHAT_ID = "-1004299364641"

TOKEN = os.environ.get("TG_BOT_TOKEN_DIESEL")
if not TOKEN:
    sys.exit("TG_BOT_TOKEN_DIESEL not set")

API = f"https://api.telegram.org/bot{TOKEN}"
TZ_MSK = timezone(timedelta(hours=3))


def send_photo(path, caption, timeout=60):
    with open(path, "rb") as f:
        r = requests.post(f"{API}/sendPhoto",
                          data={"chat_id": CHAT_ID, "caption": caption},
                          files={"photo": ("diesel.png", f, "image/png")},
                          timeout=timeout)
    return r


def send_text(text, timeout=60):
    return requests.post(f"{API}/sendMessage",
                         data={"chat_id": CHAT_ID, "parse_mode": "HTML", "text": text},
                         timeout=timeout)


def log_response(label, r):
    # 408/timeout не фейл — см. память проекта
    status = r.status_code if hasattr(r, "status_code") else "TIMEOUT"
    body = (r.text[:400] if hasattr(r, "text") else str(r))
    print(f"[{label}] status={status} body={body}")
    return status == 200 and r.json().get("ok") is True


# ── Шаг 1. Карта ──────────────────────────────────────────────
mtime = os.path.getmtime(MAP_PATH)
age_h = (time.time() - mtime) / 3600
print(f"map age: {age_h:.1f}h")
if age_h > 24:
    print("regenerating map...")
    r = subprocess.run(["python3", GEN_SCRIPT], capture_output=True, text=True)
    print(r.stdout[-400:] if r.stdout else "")
    if r.returncode != 0:
        print("gen failed:", r.stderr[-400:])
        sys.exit(1)
    if os.path.exists(MAP_SRC):
        shutil.copy2(MAP_SRC, MAP_PATH)
        print("map copied")
    else:
        sys.exit(f"gen ok but {MAP_SRC} missing")

# ── Шаг 2. Изменения за 24ч ────────────────────────────────────
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

cur.execute("""SELECT COUNT(*) FROM restrictions
               WHERE updated_at >= datetime('now','-1 day')
               AND previous_value IS NOT NULL""")
changed = cur.fetchone()[0]

cur.execute("""SELECT COUNT(*) FROM restrictions
               WHERE updated_at >= datetime('now','-1 day')
               AND previous_value IS NULL""")
new_recs = cur.fetchone()[0]

cur.execute("""SELECT region, network, city, limit_type, previous_value, limit_value
               FROM restrictions
               WHERE updated_at >= datetime('now','-1 day') AND previous_value IS NOT NULL
               ORDER BY updated_at DESC""")
changed_rows = cur.fetchall()

cur.execute("""SELECT region, network, city, limit_type, limit_value
               FROM restrictions
               WHERE updated_at >= datetime('now','-1 day') AND previous_value IS NULL
               ORDER BY updated_at DESC""")
new_rows = cur.fetchall()

cur.execute("SELECT COUNT(*) FROM prices WHERE updated_at >= datetime('now','-1 day')")
prices_upd = cur.fetchone()[0]
cur.execute("SELECT region, price FROM prices WHERE updated_at >= datetime('now','-1 day')")
prices_rows = cur.fetchall()

# Общая статистика для подписи карты
total_active = cur.execute("SELECT COUNT(*) FROM restrictions WHERE is_current=1").fetchone()[0]
total_regions = cur.execute("SELECT COUNT(DISTINCT region) FROM restrictions WHERE is_current=1").fetchone()[0]
prices_total = cur.execute("SELECT COUNT(*) FROM prices").fetchone()[0]
avg_price = cur.execute("SELECT ROUND(AVG(price),2) FROM prices").fetchone()[0] or 0
con.close()

print(f"changed={changed} new={new_recs} prices_updated={prices_upd}")
print(f"total_active={total_active} regions={total_regions} prices_total={prices_total} avg={avg_price}")

# ── Шаг 3. Публикация карты ────────────────────────────────────
now_msk = datetime.now(TZ_MSK)
caption = (
    f"Карта ограничений продажи дизеля в России на {now_msk.strftime('%d.%m.%Y')}. "
    f"Данные Росстата и сети АЗС."
)
print(f"caption: {caption}")

# Telegram не принимает PHOTO_INVALID_DIMENSIONS — ресайзим до 1280px (как в publish_diesel_map.py)
TG_IMG = "/tmp/diesel_tg.png"
try:
    img = Image.open(MAP_PATH)
    img.thumbnail((1280, 1280), Image.LANCZOS)
    img.save(TG_IMG, "PNG")
    print(f"resized for TG: {img.size}")
except Exception as e:
    print(f"resize failed: {e}, using original")
    TG_IMG = MAP_PATH

r = send_photo(TG_IMG, caption)
if not log_response("sendPhoto", r):
    sys.exit("sendPhoto failed")

# ── Шаг 4. Summary (только если есть дельты) ───────────────────
has_changes = (changed + new_recs + prices_upd) > 0
summary_lines = []

if has_changes:
    summary_lines.append(f"Изменения за сутки ({now_msk.strftime('%d.%m.%Y %H:%M')} МСК):")

    if changed:
        summary_lines.append(f"\nОбновлено ограничений: {changed}")
        # Группируем по region для читаемости
        by_region = {}
        for row in changed_rows:
            by_region.setdefault(row["region"], []).append(row)
        for region, rows in list(by_region.items())[:10]:
            nets = ", ".join(sorted({r["network"] for r in rows if r["network"]}))
            deltas = []
            for r_ in rows[:3]:
                deltas.append(f"{r_['previous_value']} -> {r_['limit_value']}")
            extra = f" и еще {len(rows)-3}" if len(rows) > 3 else ""
            summary_lines.append(f"  {region}{f' ({nets})' if nets else ''}: " + "; ".join(deltas) + extra)
        if len(by_region) > 10:
            summary_lines.append(f"  ... и еще {len(by_region)-10} регионов")

    if new_recs:
        summary_lines.append(f"\nНовых ограничений: {new_recs}")
        by_region = {}
        for row in new_rows:
            by_region.setdefault(row["region"], []).append(row)
        for region, rows in list(by_region.items())[:10]:
            vals = sorted({r["limit_value"] for r in rows if r["limit_value"]})
            nets = ", ".join(sorted({r["network"] for r in rows if r["network"]}))[:60]
            summary_lines.append(f"  {region}: {', '.join(vals[:3])}{f' ({nets})' if nets else ''}")
        if len(by_region) > 10:
            summary_lines.append(f"  ... и еще {len(by_region)-10} регионов")

    if prices_upd:
        summary_lines.append(f"\nОбновлено цен: {prices_upd} регионов. Средняя по РФ: {avg_price} руб/л.")

    summary_text = "\n".join(summary_lines)
    print("--- summary ---")
    print(summary_text)

    r = send_text(summary_text)
    if not log_response("sendMessage(summary)", r):
        sys.exit("summary send failed")

    # ── Шаг 5. Сохранение changelog для сайта ──────────────────
    date_str = now_msk.strftime("%d.%m.%Y %H:%M")
    with open(CHANGELOG, "w", encoding="utf-8") as f:
        f.write(summary_text + "\n")
        f.write(date_str + "\n")
    print(f"changelog saved: {CHANGELOG}")
else:
    print("no changes in 24h, summary skipped")

print("done")
