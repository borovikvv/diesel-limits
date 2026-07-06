# Графики динамики + Поиск/Таблица — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Добавить в карту дизель-лимитов графики динамики цены и истории лимитов в карточке региона, а также поиск региона, переключатель карта/таблица и фильтры по уровню и сети АЗС.

**Architecture:** Бэкенд расширяется: `dump_data_json.py` добавляет `price_spark` (агрегат цен за 30 дней) в каждый регион; новый `dump_history.py` генерирует каталог `/srv/static/history/*.json` с историей цен и лимитов по каждому региону. Фронтенд (`index.html`, единый файл) расширяется: в карточку добавляются спарклайн и таймлайн лимитов; в header — строка управления (поиск, toggle карта/таблица, фильтры); таблица рендерится из уже загруженных `FEATURES`. Состояние UI синхронизируется с URL hash.

**Tech Stack:** Python 3 (стандартная библиотека `sqlite3`, `json`), чистый JS + D3.js 7.9.0 (уже подключён), SVG. Тесты бэкенда — `pytest` поверх in-memory SQLite (БД живёт на сервере, локально её нет, поэтому тесты сами создают схему и фикстуры).

## Global Constraints

- Регионы нормализуются через `REGION_ALIASES` и `normalize_region()` в `dump_data_json.py` (см. строки 47–107). Любой новый код, читающий регионы из БД, обязан использовать ту же функцию.
- Уровень жёсткости считается функцией `calc_level(limit_text, has_source=...)` в `dump_data_json.py:120-180`. Не дублировать её логику во фронтенде — уровень приходит из `data.json`.
- Фронтенд: все вставки пользовательского контента экранируются через `esc(s)` (`index.html:686-691`). Все внешние URL — через `safeUrl()` (`index.html:692-698`). Любой новый DOM из данных обязан это соблюдать.
- XSS/SRI: D3 подключён с SRI с `crossorigin="anonymous"`. Новых внешних CDN-зависимостей НЕ добавлять — спарклайн и таблица на чистом SVG/DOM.
- БД на сервере: `DB = "/root/diesel_limits/restrictions.db"`. Тесты используют in-memory SQLite, воспроизводящий схему серверной БД (см. Task 1, Step 2 — точная схема).
- `data.json` и `russia_topo.json` в `.gitignore` (генерируются на сервере). Коммитить только исходники.
- Схема таблицы `restrictions`: `(id PK, region, city, network, client_type, limit_type, limit_value, source_url, source_date, is_current, previous_value, updated_at)` — выведено из INSERT-запросов в `update_all_data.py:166-179` и `update_all.py:200`.
- Схема таблицы `prices`: `(region, price, source_url, source_date, updated_at)` — из `dump_data_json.py:198` и CRONS.md:98-103.
- Схема таблицы `prices_history`: `(region, price, date)` — из запроса `dump_data_json.py:225-231`.
- Кодирование файлов: UTF-8, `ensure_ascii=False` (как в `dump_data_json.py:339`).
- Выходные пути на сервере: `/srv/static/data.json`, `/srv/static/history/`. Локально их нет — тесты пишут во временные файлы.

---

## File Structure

| Файл | Тип | Ответственность |
|---|---|---|
| `spark.py` | новый | Чистые функции агрегации: `build_price_spark(rows, days=30, max_points=12)` и `build_history(region, prices_rows, limits_rows)`. Без I/O, без обращения к БД — только обработка списков. Полностью тестируется без сервера. |
| `dump_data_json.py` | изменить | Импортировать `build_price_spark`, добавить `price_spark` в каждый объект `region` в `main()`. |
| `dump_history.py` | новый | Читает БД → вызывает `build_history()` → пишет `/srv/static/history/<region>.json`. Тонкая обёртка над `spark.py`, I/O + SQL. |
| `index.html` | изменить | (1) Строка управления в header. (2) `<div id="table-view">`. (3) Карточка: блоки спарклайна и таймлайна. (4) JS-функции рендера. |
| `CRONS.md` | изменить | Документировать `dump_history.py` в шаге 6 крона. |
| `README.md` | изменить | Описать новые функции. |
| `tests/test_spark.py` | новый | Юнит-тесты для `spark.py` (pytest, in-memory). |

Декомпозиция выбрана так: вся тестируемая логика агрегации вынесена в `spark.py` (без I/O, без БД) — это позволяет покрыть её тестами локально без серверной БД. Скрипты-дампера (`dump_data_json.py`, `dump_history.py`) остаются тонкими I/O-обёртками.

---

### Task 1: Создать `spark.py` — агрегация `price_spark` и `history`

**Files:**
- Create: `spark.py`
- Test: `tests/test_spark.py`

**Interfaces:**
- Produces:
  - `build_price_spark(rows, days=30, max_points=12) -> list[float]` — принимает список кортежей `(date_str, price)`, где `date_str` в формате `"YYYY-MM-DD"`; возвращает список цен (float), равномерно сэмплированный до `max_points` за последние `days` дней от самой свежей даты в `rows`. Если `rows` пусто — `[]`. Если точек ≤ `max_points` — все цены по порядку. Сортировка по дате asc.
  - `build_history(region, prices_rows, limits_rows) -> dict` — принимает `region` (str), `prices_rows` — список `(date_str, price)`, `limits_rows` — список `(date_str, network, old_value, new_value)`; возвращает `{"region": region, "prices": [{"date","price"}, ...], "limits": [{"date","network","old","new"}, ...]}` с `prices` отсортированными по дате asc (за 90 дней) и `limits` отсортированными по дате desc.

- [ ] **Step 1: Создать каталог `tests/` и файл теста**

Создать `tests/test_spark.py`:

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from spark import build_price_spark, build_history


def test_price_spark_empty():
    assert build_price_spark([]) == []


def test_price_spark_few_points_returned_all():
    # 3 точки — меньше max_points, вернуть все по порядку
    rows = [("2026-06-01", 60.0), ("2026-06-05", 61.0), ("2026-06-10", 62.0)]
    assert build_price_spark(rows) == [60.0, 61.0, 62.0]


def test_price_spark_downsamples_to_max_points():
    # 24 точки → сэмплировать до 12
    rows = [("2026-06-%02d" % (d+1), 60.0 + d) for d in range(24)]
    result = build_price_spark(rows, days=30, max_points=12)
    assert len(result) == 12
    # первая точка = минимальная цена (раньшая дата), последняя = последняя
    assert result[0] == 60.0
    assert result[-1] == 83.0  # 60 + 23


def test_price_spark_filters_last_30_days():
    # точки за 60 дней, но days=30 → только последние 30 дней учитываются
    rows = [("2026-05-01", 50.0), ("2026-06-25", 70.0)]
    # самая свежая дата = 2026-06-25, отсечка = 2026-05-26; 2026-05-01 отбрасывается
    result = build_price_spark(rows, days=30, max_points=12)
    assert result == [70.0]


def test_history_prices_sorted_asc_limits_desc():
    prices = [("2026-06-02", 61.0), ("2026-06-01", 60.0)]
    limits = [
        ("2026-06-01", "Газпромнефть", "100 л", "60 л"),
        ("2026-06-05", "Лукойл", None, "40 л"),
    ]
    h = build_history("Московская область", prices, limits)
    assert h["region"] == "Московская область"
    assert h["prices"] == [
        {"date": "2026-06-01", "price": 60.0},
        {"date": "2026-06-02", "price": 61.0},
    ]
    assert h["limits"] == [
        {"date": "2026-06-05", "network": "Лукойл", "old": None, "new": "40 л"},
        {"date": "2026-06-01", "network": "Газпромнефть", "old": "100 л", "new": "60 л"},
    ]


def test_history_empty_inputs():
    h = build_history("Чукотский АО", [], [])
    assert h == {"region": "Чукотский АО", "prices": [], "limits": []}
```

- [ ] **Step 2: Запустить тест, убедиться что падает (модуль не существует)**

Run: `python3 -m pytest tests/test_spark.py -v`
Expected: collection error / ImportError: No module named 'spark'.

Если pytest не установлен — установить: `python3 -m pip install pytest` (однократно, в окружение пользователя).

- [ ] **Step 3: Создать `spark.py` с реализацией**

Создать `spark.py`:

```python
"""Чистые функции агрегации для дизель-лимитов.

Без I/O, без обращения к БД — только обработка списков.
Используется dump_data_json.py (price_spark) и dump_history.py (полная история).
"""
from datetime import datetime, timedelta


def _parse_date(s):
    """'YYYY-MM-DD' → datetime.date. None/unparseable → None."""
    if not s:
        return None
    try:
        return datetime.strptime(str(s).strip(), "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def build_price_spark(rows, days=30, max_points=12):
    """Агрегирует историю цен в массив для спарклайна.

    rows: iterable of (date_str, price) — date_str в формате 'YYYY-MM-DD'.
    Возвращает list[float] длинной ≤ max_points за последние `days` дней
    от самой свежей даты в rows. Равномерное сэмплирование, сортировка asc.
    Пустой ввод → [].
    """
    parsed = []
    for date_str, price in rows:
        d = _parse_date(date_str)
        if d is None:
            continue
        try:
            p = float(price)
        except (TypeError, ValueError):
            continue
        if p <= 0 or p >= 1000:  # фильтр мусора, как в dump_data_json.normalize_price
            continue
        parsed.append((d, p))
    if not parsed:
        return []

    parsed.sort(key=lambda x: x[0])
    latest = parsed[-1][0]
    cutoff = latest - timedelta(days=days)
    window = [(d, p) for d, p in parsed if d >= cutoff]
    if not window:
        return []

    if len(window) <= max_points:
        return [p for _, p in window]

    # Равномерное сэмплирование: берём индексы 0, step, 2*step, ..., последний
    step = (len(window) - 1) / (max_points - 1)
    sampled = []
    for i in range(max_points):
        idx = int(round(i * step))
        sampled.append(window[idx][1])
    return sampled


def build_history(region, prices_rows, limits_rows):
    """Собирает объект истории региона для /static/history/<region>.json.

    prices_rows: iterable of (date_str, price).
    limits_rows: iterable of (date_str, network, old_value, new_value).
    Возвращает dict с prices (asc, за 90 дней) и limits (desc).
    """
    parsed_prices = []
    for date_str, price in prices_rows:
        d = _parse_date(date_str)
        if d is None:
            continue
        try:
            p = float(price)
        except (TypeError, ValueError):
            continue
        if p <= 0 or p >= 1000:
            continue
        parsed_prices.append((d, p))
    parsed_prices.sort(key=lambda x: x[0])
    if parsed_prices:
        cutoff = parsed_prices[-1][0] - timedelta(days=90)
        parsed_prices = [(d, p) for d, p in parsed_prices if d >= cutoff]
    prices = [{"date": d.isoformat(), "price": p} for d, p in parsed_prices]

    parsed_limits = []
    for date_str, network, old_value, new_value in limits_rows:
        d = _parse_date(date_str)
        if d is None:
            continue
        parsed_limits.append((d, network or "все сети", old_value, new_value))
    parsed_limits.sort(key=lambda x: x[0], reverse=True)
    limits = [
        {"date": d.isoformat(), "network": net, "old": old_v, "new": new_v}
        for d, net, old_v, new_v in parsed_limits
    ]

    return {"region": region, "prices": prices, "limits": limits}
```

- [ ] **Step 4: Запустить тесты, убедиться что проходят**

Run: `python3 -m pytest tests/test_spark.py -v`
Expected: 5 passed.

- [ ] **Step 5: Закоммитить**

```bash
git add spark.py tests/test_spark.py
git commit -m "feat: spark.py — агрегация price_spark и history (TDD)"
```

---

### Task 2: Расширить `dump_data_json.py` — `price_spark` в `data.json`

**Files:**
- Modify: `dump_data_json.py` (функция `main()`, ~строки 184-357)
- Test: `tests/test_spark.py` (уже покрывает агрегацию; здесь — проверка интеграции через структуру вывода)

**Interfaces:**
- Consumes: `spark.build_price_spark(rows, days=30, max_points=12)` из Task 1.
- Produces: каждый объект в `data.json["regions"]` получает поле `"price_spark": list[float]` (может быть пустым списком).

- [ ] **Step 1: Добавить импорт в начало `dump_data_json.py`**

В секции импортов (после строки `import re` ~строка 39, или рядом с другими импортами) добавить:

```python
from spark import build_price_spark
```

- [ ] **Step 2: Собрать историю цен по регионам внутри `main()`**

В функции `main()`, **после** блока чтения `weekly_changes` (после строки ~233, после `except sqlite3.OperationalError: pass`) и **до** цикла `for name in sorted(all_names):`, добавить:

```python
    # История цен для спарклайнов (price_spark)
    price_history_by_region = {}
    try:
        for r in db.execute(
            "SELECT region, date, price FROM prices_history "
            "WHERE date >= date('now','-35 days') ORDER BY date"
        ):
            name = normalize_region(r[0])
            if name:
                price_history_by_region.setdefault(name, []).append((r[1], r[2]))
    except sqlite3.OperationalError:
        pass  # таблицы prices_history может не быть — спарклайны будут пустыми
```

- [ ] **Step 3: Добавить `price_spark` в объект региона**

Найти в `main()` место, где формируется `regions.append({...})` (~строки 292-299) и добавить поле `price_spark`. Заменить:

```python
        regions.append({
            "region": name,
            "level": level,
            "price": price,
            "limit_text": limit_text,
            "truck_limits": truck_limits,
            "weekly_change": weekly_changes.get(name)
        })
```

на:

```python
        spark_rows = price_history_by_region.get(name, [])
        regions.append({
            "region": name,
            "level": level,
            "price": price,
            "limit_text": limit_text,
            "truck_limits": truck_limits,
            "weekly_change": weekly_changes.get(name),
            "price_spark": build_price_spark(spark_rows)
        })
```

- [ ] **Step 4: Проверить синтаксис**

Run: `python3 -c "import ast; ast.parse(open('dump_data_json.py').read()); print('OK')"`
Expected: `OK`

- [ ] **Step 5: Закоммитить**

```bash
git add dump_data_json.py
git commit -m "feat: price_spark в data.json (спарклайн цены за 30 дней)"
```

---

### Task 3: Создать `dump_history.py` — каталог `/srv/static/history/*.json`

**Files:**
- Create: `dump_history.py`
- Test: `tests/test_dump_history.py`

**Interfaces:**
- Consumes: `spark.build_history(region, prices_rows, limits_rows)` из Task 1; `normalize_region()` из `dump_data_json.py`.
- Produces: файл `/srv/static/history/<URL-encoded region>.json` на каждый регион с актуальными ограничениями. Формат: `{"region", "prices": [{"date","price"}], "limits": [{"date","network","old","new"}]}`.

**Контекст (схема БД — выведено из кода):**
- `prices_history`: `(region, price, date)`.
- `restrictions`: содержит `region, network, source_date, limit_value, previous_value, is_current`. История изменений = все строки, у которых `previous_value IS NOT NULL`, плюс текущее значение (`limit_value`) каждой текущей записи как «новое». `previous_value` = значение до последнего изменения (одно), а сам таймлайн восстанавливается из набора записей с их `source_date`.

- [ ] **Step 1: Написать тест на `dump_history.py` через in-memory SQLite**

Создать `tests/test_dump_history.py`:

```python
import sys, os, json, sqlite3, urllib.parse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import dump_history


SCHEMA = """
CREATE TABLE prices_history (region TEXT, price REAL, date TEXT);
CREATE TABLE restrictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region TEXT, city TEXT, network TEXT, client_type TEXT,
    limit_type TEXT, limit_value TEXT, source_url TEXT, source_date TEXT,
    is_current INTEGER, previous_value TEXT, updated_at TEXT
);
"""


def make_db():
    db = sqlite3.connect(":memory:")
    db.executescript(SCHEMA)
    return db


def test_collect_history_returns_region_data():
    db = make_db()
    db.executemany(
        "INSERT INTO prices_history(region,price,date) VALUES(?,?,?)",
        [("Москва", 60.0, "2026-06-01"), ("Москва", 62.0, "2026-06-10")],
    )
    db.executemany(
        "INSERT INTO restrictions(region,network,source_date,limit_value,previous_value,is_current) "
        "VALUES(?,?,?,?,?,?)",
        [("Москва", "Газпромнефть", "2026-06-05", "60 л", "100 л", 1)],
    )
    out = dump_history.collect_for_region(db, "Москва")
    assert out["region"] == "Москва"
    assert out["prices"] == [
        {"date": "2026-06-01", "price": 60.0},
        {"date": "2026-06-10", "price": 62.0},
    ]
    assert out["limits"] == [
        {"date": "2026-06-05", "network": "Газпромнефть", "old": "100 л", "new": "60 л"},
    ]


def test_collect_history_empty_region():
    db = make_db()
    out = dump_history.collect_for_region(db, "Чукотский АО")
    assert out == {"region": "Чукотский АО", "prices": [], "limits": []}


def test_write_history_files_creates_one_per_region(tmp_path):
    db = make_db()
    db.executemany(
        "INSERT INTO prices_history(region,price,date) VALUES(?,?,?)",
        [("Москва", 60.0, "2026-06-01")],
    )
    db.execute(
        "INSERT INTO restrictions(region,network,source_date,limit_value,is_current) "
        "VALUES('Москва','Лукойл','2026-06-01','40 л',1)"
    )
    out_dir = tmp_path / "history"
    dump_history.write_all(db, str(out_dir))
    files = list(out_dir.iterdir())
    assert len(files) == 1
    # имя файла = URL-encoded регион
    expected_name = urllib.parse.quote("Москва", safe="") + ".json"
    assert files[0].name == expected_name
    data = json.loads(files[0].read_text(encoding="utf-8"))
    assert data["region"] == "Москва"
    assert len(data["prices"]) == 1
```

- [ ] **Step 2: Запустить тест, убедиться что падает**

Run: `python3 -m pytest tests/test_dump_history.py -v`
Expected: ImportError: No module named 'dump_history'.

- [ ] **Step 3: Создать `dump_history.py`**

Создать `dump_history.py`:

```python
#!/usr/bin/env python3
"""Генерирует каталог /srv/static/history/<region>.json — по файлу на регион.

Каждый файл: {"region", "prices": [...], "limits": [...]}.
Запускается после dump_data_json.py в кроне diesel-heatmap-daily.
"""
import sqlite3
import os
import sys
import urllib.parse

# Импортируем из соседних модулей репозитория
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spark import build_history
from dump_data_json import normalize_region

DB = "/root/diesel_limits/restrictions.db"
OUT_DIR = "/srv/static/history"


def collect_for_region(db, region):
    """Собирает объект истории одного региона из БД.

    db: открытое sqlite3-подключение.
    region: нормализованное имя региона.
    Возвращает dict, готовый для json.dump.
    """
    prices_rows = db.execute(
        "SELECT date, price FROM prices_history WHERE region=? ORDER BY date",
        (region,),
    ).fetchall()
    limits_rows = db.execute(
        "SELECT source_date, network, previous_value, limit_value "
        "FROM restrictions WHERE region=? AND source_date IS NOT NULL "
        "ORDER BY source_date DESC",
        (region,),
    ).fetchall()
    return build_history(region, prices_rows, limits_rows)


def write_all(db, out_dir):
    """Пишет по файлу <region>.json на каждый регион с актуальными ограничениями.

    Имя файла = urllib.parse.quote(region, safe='') + '.json'.
    Создаёт out_dir при отсутствии.
    """
    os.makedirs(out_dir, exist_ok=True)
    regions = [
        r[0] for r in db.execute(
            "SELECT DISTINCT region FROM restrictions WHERE is_current=1"
        ).fetchall()
        if r[0]
    ]
    # Добавим регионы, у которых есть цены, но нет ограничений — для полноты спарклайна
    price_regions = [
        r[0] for r in db.execute(
            "SELECT DISTINCT region FROM prices_history"
        ).fetchall()
        if r[0]
    ]
    seen = set()
    for raw in regions + price_regions:
        name = normalize_region(raw)
        if not name or name in seen:
            continue
        seen.add(name)
        data = collect_for_region(db, name)
        fname = urllib.parse.quote(name, safe="") + ".json"
        path = os.path.join(out_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            import json
            json.dump(data, f, ensure_ascii=False)
        os.chmod(path, 0o644)


def main():
    db = sqlite3.connect(DB)
    try:
        write_all(db, OUT_DIR)
    finally:
        db.close()
    # Подсчёт для лога крона
    n = len([f for f in os.listdir(OUT_DIR) if f.endswith(".json")]) if os.path.isdir(OUT_DIR) else 0
    print(f"dump_history: {n} region files written to {OUT_DIR}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Запустить тесты, убедиться что проходят**

Run: `python3 -m pytest tests/test_dump_history.py tests/test_spark.py -v`
Expected: 8 passed (5 + 3).

- [ ] **Step 5: Проверить синтаксис обоих дампера**

Run: `python3 -c "import ast; ast.parse(open('dump_history.py').read()); ast.parse(open('dump_data_json.py').read()); print('OK')"`
Expected: `OK`

- [ ] **Step 6: Закоммитить**

```bash
git add dump_history.py tests/test_dump_history.py
git commit -m "feat: dump_history.py — каталог истории по регионам"
```

---

### Task 4: Фронтенд — спарклайн цены в карточке региона

**Files:**
- Modify: `index.html` (CSS в `<style>`, JS в `showRegionCard()` ~строки 1116-1181, парсинг `price_spark` в `loadData()` ~строки 658-670)

**Interfaces:**
- Consumes: `data.json` с полем `price_spark: list[float]` в каждом регионе (Task 2).
- Produces: в `.region-card` добавляется блок спарклайна под ценой.

**Контекст:** Карточка рендерится функцией `showRegionCard(d)` (`index.html:1116`). Данные региона приходят в объекте `d` с полями `region, level, price, limit_text, truck_limits, weekly_change`. Нужно добавить поле `price_spark`.

- [ ] **Step 1: Добавить `price_spark` в парсинг `loadData()`**

В `index.html` найти в `loadData()` (около строки 658-670) `return {...}` и добавить поле. Заменить:

```javascript
      return {
        region: name,
        level: data.level != null ? data.level : -1,
        price: data.price || null,
        limit_text: data.limit_text || "Нет данных",
        truck_limits: data.truck_limits || [],
        weekly_change: data.weekly_change || null,
        geometry: f.geometry
      };
```

на:

```javascript
      return {
        region: name,
        level: data.level != null ? data.level : -1,
        price: data.price || null,
        limit_text: data.limit_text || "Нет данных",
        truck_limits: data.truck_limits || [],
        weekly_change: data.weekly_change || null,
        price_spark: Array.isArray(data.price_spark) ? data.price_spark : [],
        geometry: f.geometry
      };
```

- [ ] **Step 2: Добавить CSS для спарклайна**

В `<style>` (например, после блока `.price-change` ~строка 247) добавить:

```css
  .region-card .spark-wrap {
    margin-top: 8px;
  }
  .region-card .spark-svg {
    display: block;
    width: 100%;
    height: 32px;
  }
  .region-card .spark-line {
    fill: none;
    stroke-width: 2;
    vector-effect: non-scaling-stroke;
  }
  .region-card .spark-stats {
    font-size: 10px;
    color: #64748B;
    margin-top: 3px;
  }
```

- [ ] **Step 3: Добавить JS-функцию рендера спарклайна**

Вставить **перед** функцией `showRegionCard` (перед строкой 1116) новую функцию:

```javascript
  // === Спарклайн цены: чистый SVG polyline ===
  function renderSparkline(values){
    // values: number[] (цены). Возвращает HTML-строку блока спарклайна + статистики.
    if(!values || values.length < 2){
      return '';  // недостаточно данных для линии
    }
    const W = 120, H = 28, pad = 2;
    const min = Math.min(...values), max = Math.max(...values);
    const range = (max - min) || 1;
    const stepX = (W - pad*2) / (values.length - 1);
    const pts = values.map((v, i) => {
      const x = pad + i * stepX;
      const y = H - pad - ((v - min) / range) * (H - pad*2);
      return x.toFixed(1) + "," + y.toFixed(1);
    }).join(" ");
    // Цвет по тренду
    const first = values[0], last = values[values.length-1];
    let color = "#64748B";  // ровно
    if(last - first > 0.01) color = "#EF4444";       // рост → красный
    else if(last - first < -0.01) color = "#10B981"; // падение → зелёный
    const avg = values.reduce((a,b) => a+b, 0) / values.length;
    return `
      <div class="spark-wrap">
        <svg class="spark-svg" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" aria-hidden="true">
          <polyline class="spark-line" stroke="${color}" points="${pts}"></polyline>
        </svg>
        <div class="spark-stats">мин ${min.toFixed(2)} · макс ${max.toFixed(2)} · сред ${avg.toFixed(2)}</div>
      </div>
    `;
  }
```

- [ ] **Step 4: Вставить спарклайн в карточку**

В `showRegionCard(d)` найти место формирования `priceText` (около строки 1118-1120) и добавить рендер спарклайна. Заменить:

```javascript
    const priceText = d.price != null
      ? `<div class="price-block"><span class="price">${esc(d.price.toFixed(2))}</span><span class="unit">руб/л</span></div>`
      : `<div class="price-block"><span class="price" style="color:#64748B">нет данных</span></div>`;
    const changeText = d.weekly_change != null && d.weekly_change > 0
      ? `<span class="price-change">↑ +${d.weekly_change.toFixed(2)} ₽/л за неделю</span>`
      : '';
```

на:

```javascript
    const priceText = d.price != null
      ? `<div class="price-block"><span class="price">${esc(d.price.toFixed(2))}</span><span class="unit">руб/л</span></div>`
      : `<div class="price-block"><span class="price" style="color:#64748B">нет данных</span></div>`;
    const changeText = d.weekly_change != null && d.weekly_change > 0
      ? `<span class="price-change">↑ +${d.weekly_change.toFixed(2)} ₽/л за неделю</span>`
      : '';
    const sparkHtml = renderSparkline(d.price_spark);
```

Затем в шаблоне `els.card.innerHTML` найти секцию цены и добавить `${sparkHtml}`. Заменить:

```javascript
        <div class="card-section">
          <h4>Цена ДТ</h4>
          ${priceText}
          ${changeText}
        </div>
```

на:

```javascript
        <div class="card-section">
          <h4>Цена ДТ</h4>
          ${priceText}
          ${changeText}
          ${sparkHtml}
        </div>
```

- [ ] **Step 5: Проверить в браузере (без сервера — мок)**

Открыть `index.html` нельзя напрямую из-за `fetch('/static/data.json')`. Для ручной проверки в `loadData()` временно подменить fetch на мок (НЕ коммитить это изменение):

Временно вставить после `try{` в `loadData()`:
```javascript
    // ВРЕМЕННЫЙ МОК ДЛЯ ПРОВЕРКИ — удалить перед коммитом
    const d = { updated: "06.07.2026", changelog: "тест", regions: [
      { region: "Москва", level: 2, price: 68.45, weekly_change: 1.2, price_spark: [67.1, 67.3, 67.5, 67.8, 68.0, 68.45], limit_text: "60 л", truck_limits: [] }
    ]};
```
…закомментировать реальные fetch'и, открыть `index.html` в браузере, кликнуть «Москва», убедиться что спарклайн виден под ценой и окрашен красным (рост). После проверки — `git checkout index.html` чтобы откатить мок.

Expected: под ценой видна ломаная линия 6 точек, цвет красный, подпись «мин 67.10 · макс 68.45 · сред 67.69».

- [ ] **Step 6: Закоммитить**

```bash
git add index.html
git commit -m "feat: спарклайн цены в карточке региона (30 дней)"
```

---

### Task 5: Фронтенд — таймлайн лимитов (lazy-загрузка истории)

**Files:**
- Modify: `index.html` (CSS, JS в `showRegionCard()`)

**Interfaces:**
- Consumes: `/static/history/<region>.json` (Task 3), формат `{"region", "prices": [...], "limits": [{"date","network","old","new"}]}`.
- Produces: в карточке появляется блок «История изменений» под блоком «Для грузовиков».

- [ ] **Step 1: Добавить CSS для таймлайна**

В `<style>` (после блока `.truck-block` ~строка 273) добавить:

```css
  .region-card .timeline-block {
    margin-top: 4px;
  }
  .region-card .timeline-item {
    padding: 6px 8px;
    border-bottom: 1px solid #F1F5F9;
    font-size: 11px;
    line-height: 1.4;
  }
  .region-card .timeline-item:last-child { border-bottom: none; }
  .region-card .timeline-item .tl-date {
    color: #64748B;
    font-size: 10px;
  }
  .region-card .timeline-item .tl-net {
    font-weight: 600;
    color: #1E293B;
    margin-left: 6px;
  }
  .region-card .timeline-item .tl-change {
    display: flex;
    align-items: center;
    gap: 4px;
    margin-top: 2px;
  }
  .region-card .timeline-item .tl-arrow { font-weight: 700; }
  .region-card .timeline-item.tighten .tl-arrow { color: #EF4444; }
  .region-card .timeline-item.loosen  .tl-arrow { color: #10B981; }
  .region-card .timeline-item.newlim  .tl-arrow { color: #F59E0B; }
  .region-card .timeline-loading {
    font-size: 11px;
    color: #64748B;
    font-style: italic;
    padding: 6px 8px;
  }
  .region-card .timeline-error {
    font-size: 11px;
    color: #94A3B8;
    padding: 6px 8px;
  }
```

- [ ] **Step 2: Добавить JS-функцию классификации и рендера таймлайна**

Вставить **перед** функцией `showRegionCard` (рядом с `renderSparkline` из Task 4):

```javascript
  // === Классификация изменения лимита ===
  function firstLiters(text){
    // Извлекает первое число перед 'л' (минимум из диапазона). null если нет.
    if(!text) return null;
    const m = String(text).match(/(\d+)\s*[-–/]?\s*\d*\s*л/);
    return m ? parseInt(m[1], 10) : null;
  }
  function classifyLimitChange(oldV, newV){
    // Возвращает {cls, arrow}: cls ∈ {'tighten','loosen','newlim','remove','change'}, arrow — символ
    const oldN = firstLiters(oldV);
    const newN = firstLiters(newV);
    if(oldV == null && newV != null) return {cls: "newlim", arrow: "▼"};        // новое ограничение
    if(newV != null && /без огранич|нет огранич|свободн/i.test(newV)) return {cls: "loosen", arrow: "▲"}; // снятие
    if(oldN != null && newN != null){
      if(newN < oldN) return {cls: "tighten", arrow: "▼"};   // ужесточение
      if(newN > oldN) return {cls: "loosen",  arrow: "▲"};   // послабление
    }
    return {cls: "change", arrow: "•"};  // неколичественное изменение
  }
  function renderTimeline(limits){
    // limits: [{date,network,old,new}] отсортированы desc. Возвращает HTML.
    if(!limits || limits.length === 0){
      return '<div class="timeline-loading">изменений не было</div>';
    }
    return limits.map(it => {
      const {cls, arrow} = classifyLimitChange(it.old, it.new);
      const oldTxt = it.old ? esc(it.old) : '—';
      const newTxt = it.new ? esc(it.new) : 'без ограничений';
      return `
        <div class="timeline-item ${cls}">
          <span class="tl-date">${esc(it.date)}</span>
          <span class="tl-net">${esc(it.network)}</span>
          <div class="tl-change">
            <span>${oldTxt}</span>
            <span class="tl-arrow">${arrow}</span>
            <span>${newTxt}</span>
          </div>
        </div>
      `;
    }).join('');
  }
```

- [ ] **Step 3: Добавить блок таймлайна в карточку с lazy-загрузкой**

В `showRegionCard(d)` найти закрывающую часть шаблона (блок `truckBlock` вставляется перед `</div>` карточки). Заменить конец шаблона. Найти:

```javascript
        ${truckBlock}
      </div>
    `;
    els.card.classList.add("visible");
```

и заменить на:

```javascript
        ${truckBlock}
        <div class="card-section">
          <h4>История изменений</h4>
          <div class="timeline-block" id="timeline-block">
            <div class="timeline-loading">загрузка истории…</div>
          </div>
        </div>
      </div>
    `;
    els.card.classList.add("visible");

    // Lazy-загрузка истории лимитов
    (async () => {
      const tl = els.card.querySelector("#timeline-block");
      if(!tl) return;
      try {
        const url = "/static/history/" + encodeURIComponent(d.region) + ".json";
        const r = await fetch(url);
        if(!r.ok) throw new Error("HTTP " + r.status);
        const h = await r.json();
        tl.innerHTML = renderTimeline(h.limits);
      } catch(e){
        console.warn("history load failed for", d.region, e);
        tl.innerHTML = '<div class="timeline-error">история недоступна</div>';
      }
    })();
```

- [ ] **Step 4: Проверить в браузере (без сервера — мок fetch)**

В `loadData()` временно подменить **один из** fetch'ей (history) через заглушку. После `els.card.classList.add("visible");` временно нельзя перехватить — поэтому проще: временно переопределить `fetch` в начале `<script>` (НЕ коммитить):

```javascript
// ВРЕМЕННЫЙ МОК — удалить перед коммитом
const _origFetch = window.fetch;
window.fetch = function(url){
  if(typeof url === 'string' && url.startsWith('/static/history/')){
    return Promise.resolve(new Response(JSON.stringify({
      region: "Москва",
      prices: [],
      limits: [
        {date:"2026-06-15", network:"Газпромнефть", old:"100 л", new:"60 л"},
        {date:"2026-06-20", network:"Лукойл", old:null, new:"40 л"},
        {date:"2026-07-01", network:"Роснефть", old:"40 л", new:"100 л"}
      ]
    }), {status:200, headers:{'Content-Type':'application/json'}}));
  }
  return _origFetch.apply(this, arguments);
};
```
Открыть страницу, кликнуть регион — убедиться что таймлайн рендерится: три записи, первая запись (Газпромнефть 100→60) с красной ▼, вторая (Лукойл —→40) с оранжевой ▼, третья (Роснефть 40→100) с зелёной ▲. После проверки — `git checkout index.html`.

Expected: блок «История изменений» содержит 3 цветных записи.

- [ ] **Step 5: Закоммитить**

```bash
git add index.html
git commit -m "feat: таймлайн лимитов в карточке (lazy /static/history/)"
```

---

### Task 6: Фронтенд — поиск региона

**Files:**
- Modify: `index.html` (HTML в `header`, CSS, JS)

**Interfaces:**
- Consumes: `FEATURES` (уже загружены).
- Produces: поле поиска с автодополнением; при выборе — зум к региону на карте + открытие карточки.

- [ ] **Step 1: Добавить HTML строки управления в `header`**

В `header` (после `</div>` блока `.stats` ~строка 517, перед `</header>`) добавить:

```html
    <div class="toolbar" role="search">
      <div class="search-wrap">
        <input id="region-search" type="search" placeholder="🔍 Поиск региона…"
               aria-label="Поиск региона" autocomplete="off"
               list="region-list" />
        <datalist id="region-list"></datalist>
        <button id="search-clear" type="button" aria-label="Очистить поиск" hidden>×</button>
      </div>
      <div id="view-toggle" class="view-toggle" role="group" aria-label="Вид данных">
        <button id="view-map-btn" type="button" class="active" aria-pressed="true">🗺️ Карта</button>
        <button id="view-table-btn" type="button" aria-pressed="false">📋 Таблица</button>
      </div>
    </div>
```

- [ ] **Step 2: Добавить CSS для тулбара и поиска**

В `<style>` (после блока `header .stats` ~строка 75) добавить:

```css
  .toolbar {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    width: 100%;
    margin-top: 8px;
  }
  .toolbar .search-wrap {
    position: relative;
    flex: 1;
    min-width: 200px;
    max-width: 360px;
  }
  .toolbar #region-search {
    width: 100%;
    padding: 6px 28px 6px 10px;
    font-size: 13px;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    background: #F8FAFC;
  }
  .toolbar #region-search:focus {
    outline: 2px solid #2563EB;
    outline-offset: -1px;
    background: white;
  }
  .toolbar #search-clear {
    position: absolute;
    right: 6px;
    top: 50%;
    transform: translateY(-50%);
    border: none;
    background: #CBD5E1;
    color: white;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 12px;
    line-height: 1;
  }
  .toolbar .view-toggle {
    display: inline-flex;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    overflow: hidden;
    margin-left: auto;
  }
  .toolbar .view-toggle button {
    padding: 6px 12px;
    border: none;
    background: white;
    color: #475569;
    font-size: 12px;
    cursor: pointer;
  }
  .toolbar .view-toggle button.active {
    background: #2563EB;
    color: white;
  }
  .toolbar .view-toggle button:focus-visible {
    outline: 2px solid #2563EB;
    outline-offset: -2px;
  }
```

- [ ] **Step 3: Добавить JS логику поиска**

Внутри `drawAll()`, **после** блока `setupAccordion()` (перед блоком `// КАРТА НА D3` ~строка 866), добавить новую IIFE:

```javascript
// ============================================================
//  ПОИСК РЕГИОНА
// ============================================================
(function setupSearch(){
  const input = document.getElementById('region-search');
  const clearBtn = document.getElementById('search-clear');
  const datalist = document.getElementById('region-list');
  if(!input || !datalist) return;

  // Заполняем datalist всеми регионами
  datalist.innerHTML = FEATURES
    .map(f => `<option value="${esc(f.region)}">`)
    .join('');

  function findRegion(q){
    if(!q) return null;
    const ql = q.toLowerCase().trim();
    // точное совпадение优先, иначе подстрока
    let exact = FEATURES.find(f => f.region.toLowerCase() === ql);
    if(exact) return exact;
    return FEATURES.find(f => f.region.toLowerCase().includes(ql)) || null;
  }

  input.addEventListener('input', () => {
    if(clearBtn) clearBtn.hidden = !input.value;
  });
  if(clearBtn){
    clearBtn.addEventListener('click', () => {
      input.value = '';
      clearBtn.hidden = true;
      input.focus();
    });
  }
  input.addEventListener('change', () => {
    const f = findRegion(input.value);
    if(f){
      focusRegion(f);
      input.blur();
    }
  });
  input.addEventListener('keydown', (e) => {
    if(e.key === 'Enter'){
      const f = findRegion(input.value);
      if(f){
        focusRegion(f);
        input.blur();
      }
    }
  });
})();

// focusRegion определяется в Task 7 (по мере доступности svg/zoom).
// Заглушка, чтобы поиск работал до подключения зума:
function focusRegion(f){
  // Открываем карточку — этого достаточно как минимальное поведение.
  if(typeof showRegionCard === 'function') showRegionCard(f);
}
```

**Важно:** `focusRegion` здесь объявлен как заглушка (только карточка). В Task 8 мы расширим его до зума + карточки. Это позволяет проверить поиск уже сейчас.

- [ ] **Step 4: Проверить в браузере (мок)**

Использовать тот же временный мок `data.json`, что в Task 4, Step 5, но с несколькими регионами:
```javascript
const d = { updated: "06.07.2026", changelog: "тест", regions: [
  { region: "Москва", level: 2, price: 68.45, price_spark: [], limit_text: "60 л", truck_limits: [] },
  { region: "Республика Татарстан", level: 1, price: 65.2, price_spark: [], limit_text: "—", truck_limits: [] },
  { region: "Чукотский АО", level: -1, price: null, price_spark: [], limit_text: "Нет данных", truck_limits: [] }
]};
```
Открыть страницу, ввести «татар» в поиск, нажать Enter — карточка Татарстана открывается. Иконка очистки (×) появляется при вводе и очищает поле.

Expected: ввод «татар» → открывается карточка «Республика Татарстан».

- [ ] **Step 5: Закоммитить**

```bash
git add index.html
git commit -m "feat: поиск региона с автодополнением"
```

---

### Task 7: Фронтенд — переключатель Карта/Таблица + рендер таблицы

**Files:**
- Modify: `index.html` (HTML, CSS, JS)

**Interfaces:**
- Consumes: `FEATURES`, `LEVEL_BY_ID`, `esc()` (всё уже есть).
- Produces: `<div id="table-view">` показывается вместо `#map-wrap` при активном виде «Таблица». Сортируемая таблица 85 регионов. Клик по строке → `showRegionCard(f)`.

- [ ] **Step 1: Добавить HTML контейнера таблицы**

Внутри `#map-wrap` (после `<svg id="map-svg">` ~строка 521) добавить:

```html
      <div id="table-view" role="region" aria-label="Таблица регионов" hidden></div>
```

- [ ] **Step 2: Добавить CSS таблицы**

В `<style>` (после блока `.controls` ~строка 461) добавить:

```css
  #table-view {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    overflow: auto;
    background: white;
    -webkit-overflow-scrolling: touch;
  }
  #table-view table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
  }
  #table-view thead {
    position: sticky;
    top: 0;
    background: #F1F5F9;
    z-index: 2;
  }
  #table-view th {
    padding: 8px 10px;
    text-align: left;
    font-weight: 700;
    color: #1E293B;
    cursor: pointer;
    user-select: none;
    border-bottom: 1px solid #CBD5E1;
    white-space: nowrap;
  }
  #table-view th:focus-visible { outline: 2px solid #2563EB; outline-offset: -2px; }
  #table-view th .sort-ind { color: #2563EB; margin-left: 4px; }
  #table-view td {
    padding: 7px 10px;
    border-bottom: 1px solid #F1F5F9;
    color: #1E293B;
    vertical-align: top;
  }
  #table-view tbody tr { cursor: pointer; }
  #table-view tbody tr:hover { background: #F8FAFC; }
  #table-view tbody tr:focus-visible { outline: 2px solid #2563EB; outline-offset: -2px; }
  #table-view .lvl-badge {
    display: inline-block;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 10px;
    font-weight: 600;
    color: white;
  }
  #table-view .num-cell { text-align: right; font-variant-numeric: tabular-nums; }
  #table-view .empty-cell { color: #94A3B8; }
  #table-view .result-count {
    padding: 6px 10px;
    font-size: 11px;
    color: #64748B;
    background: #F8FAFC;
    border-bottom: 1px solid #E2E8F0;
  }
```

- [ ] **Step 3: Добавить JS-функцию рендера таблицы с сортировкой**

Внутри `drawAll()`, рядом с `setupSearch()` (после него), добавить новую IIFE и функцию:

```javascript
// ============================================================
//  ПЕРЕКЛЮЧАТЕЛЬ ВИДА: Карта / Таблица
// ============================================================
const TABLE_VIEW = {
  sortKey: 'region',
  sortDir: 1  // 1=asc, -1=desc
};

function renderTable(){
  const container = document.getElementById('table-view');
  if(!container) return;

  // FEATURES может быть отфильтрован (Task 8) — учитываем через window.__filteredFeatures
  const rows = (typeof window.__filteredFeatures !== 'undefined' && window.__filteredFeatures)
    ? window.__filteredFeatures : FEATURES;

  const sorted = [...rows].sort((a, b) => {
    let va = a[TABLE_VIEW.sortKey], vb = b[TABLE_VIEW.sortKey];
    if(TABLE_VIEW.sortKey === 'level'){ va = a.level; vb = b.level; }
    if(va == null) va = (TABLE_VIEW.sortKey === 'price' ? -Infinity : '');
    if(vb == null) vb = (TABLE_VIEW.sortKey === 'price' ? -Infinity : '');
    if(typeof va === 'number' && typeof vb === 'number'){
      return (va - vb) * TABLE_VIEW.sortDir;
    }
    return String(va).localeCompare(String(vb), 'ru') * TABLE_VIEW.sortDir;
  });

  const cols = [
    {key: 'region',  label: 'Регион'},
    {key: 'level',   label: 'Уровень'},
    {key: 'price',   label: 'Цена'},
    {key: 'limit_text', label: 'Лимит'},
    {key: 'truck',   label: 'Грузовикам'}
  ];

  const headerHtml = cols.map(c => {
    const isActive = TABLE_VIEW.sortKey === c.key;
    const ind = isActive ? `<span class="sort-ind">${TABLE_VIEW.sortDir > 0 ? '▲' : '▼'}</span>` : '';
    return `<th scope="col" data-key="${c.key}" tabindex="0">${esc(c.label)}${ind}</th>`;
  }).join('');

  const bodyHtml = sorted.map((f, i) => {
    const lv = LEVEL_BY_ID[f.level] || LEVELS[0];
    const priceCell = f.price != null
      ? `<td class="num-cell">${esc(f.price.toFixed(2))}</td>`
      : `<td class="num-cell empty-cell">—</td>`;
    const truckTxt = (f.truck_limits || [])
      .filter(t => t && t.network).slice(0, 2)
      .map(t => `${esc(t.network)}: ${esc(t.limit)}`).join('; ');
    const truckCell = truckTxt
      ? `<td>${truckTxt}</td>`
      : `<td class="empty-cell">нет данных</td>`;
    return `
      <tr tabindex="0" data-idx="${i}">
        <td>${esc(f.region)}</td>
        <td><span class="lvl-badge" style="background:${lv.color}">${esc(lv.label_short)}</span></td>
        ${priceCell}
        <td>${esc(f.limit_text || '—')}</td>
        ${truckCell}
      </tr>`;
  }).join('');

  container.innerHTML = `
    <div class="result-count" aria-live="polite">Показано ${sorted.length} из ${FEATURES.length} регионов</div>
    <table>
      <thead><tr>${headerHtml}</tr></thead>
      <tbody>${bodyHtml}</tbody>
    </table>
  `;

  // Сортировка по клику/Enter на заголовке
  container.querySelectorAll('th[data-key]').forEach(th => {
    const onActivate = () => {
      const key = th.getAttribute('data-key');
      if(TABLE_VIEW.sortKey === key){
        TABLE_VIEW.sortDir *= -1;
      } else {
        TABLE_VIEW.sortKey = key;
        TABLE_VIEW.sortDir = 1;
      }
      renderTable();
    };
    th.addEventListener('click', onActivate);
    th.addEventListener('keydown', e => {
      if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); onActivate(); }
    });
  });

  // Клик/Enter на строке → карточка
  container.querySelectorAll('tbody tr').forEach(tr => {
    const idx = parseInt(tr.getAttribute('data-idx'), 10);
    const f = sorted[idx];
    const open = () => showRegionCard(f);
    tr.addEventListener('click', open);
    tr.addEventListener('keydown', e => {
      if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); open(); }
    });
  });
}

(function setupViewToggle(){
  const mapBtn = document.getElementById('view-map-btn');
  const tblBtn = document.getElementById('view-table-btn');
  const mapView = document.querySelector('#map-wrap > #map-svg').parentElement;
  // table-view уже внутри #map-wrap; показываем/прячем relative
  const tblView = document.getElementById('table-view');
  const svgEl = document.getElementById('map-svg');
  const controls = document.querySelector('#map-wrap .controls');
  const hint = document.querySelector('#map-wrap .hint');
  if(!mapBtn || !tblBtn || !tblView) return;

  function setView(view){
    const isTable = view === 'table';
    tblView.hidden = !isTable;
    if(svgEl) svgEl.style.visibility = isTable ? 'hidden' : 'visible';
    if(controls) controls.style.display = isTable ? 'none' : '';
    if(hint) hint.style.display = isTable ? 'none' : '';
    mapBtn.classList.toggle('active', !isTable);
    tblBtn.classList.toggle('active', isTable);
    mapBtn.setAttribute('aria-pressed', String(!isTable));
    tblBtn.setAttribute('aria-pressed', String(isTable));
    if(isTable) renderTable(); else renderTable;  // перерисуем при возврате тоже (на случай фильтра)
  }

  mapBtn.addEventListener('click', () => setView('map'));
  tblBtn.addEventListener('click', () => setView('table'));

  // Экспорт для Task 8 (фильтры/URL hash)
  window.__setView = setView;
  window.__currentView = () => tblView.hidden ? 'map' : 'table';
})();
```

- [ ] **Step 4: Проверить в браузере (мок)**

Использовать мок из Task 6 с тремя регионами. Открыть страницу, нажать «📋 Таблица» — должна появиться таблица из 3 строк с цветными бейджами уровня. Клик по «Цена» → сортировка по цене, индикатор ▲. Клик по строке → открывается карточка региона. Нажать «🗺️ Карта» → таблица скрывается, карта видна.

Expected: таблица рендерится, сортируется, клик по строке открывает карточку.

- [ ] **Step 5: Закоммитить**

```bash
git add index.html
git commit -m "feat: переключатель карта/таблица + сортируемая таблица регионов"
```

---

### Task 8: Фронтенд — фильтры (уровень + сеть) + URL hash + зум к региону

**Files:**
- Modify: `index.html` (HTML, CSS, JS; расширение `focusRegion` из Task 6)

**Interfaces:**
- Consumes: `FEATURES`, `LEVELS`, `LEVEL_BY_ID`, `window.__setView`/`window.__currentView` (Task 7), `d3.zoom` (уже есть), `svg`/`g`/`zoom` (уже есть в scope `drawAll`).
- Produces:
  - Чипсы фильтра по уровню + dropdown по сети АЗС; кнопка «Сбросить».
  - Применение: карта затемняет отфильтрованные регионы (opacity 0.25); таблица скрывает строки.
  - `focusRegion(f)` расширяется: зум к региону + карточка.
  - Состояние (вид + фильтры + поиск) синхронизируется с `location.hash`.

- [ ] **Step 1: Добавить HTML фильтров в `header`**

В `header`, **после** блока `.toolbar` (из Task 6), добавить:

```html
    <div class="filters" id="filters-bar" role="group" aria-label="Фильтры">
      <div class="filter-group">
        <span class="filter-label">Уровень:</span>
        <div id="level-chips" class="chips"></div>
      </div>
      <div class="filter-group">
        <span class="filter-label">Сеть АЗС:</span>
        <select id="network-filter" aria-label="Фильтр по сети АЗС">
          <option value="">Все сети</option>
        </select>
      </div>
      <button id="filters-reset" type="button">Сбросить</button>
    </div>
```

- [ ] **Step 2: Добавить CSS для фильтров**

В `<style>` (после стилей `.toolbar`) добавить:

```css
  .filters {
    display: flex;
    align-items: center;
    gap: 14px;
    flex-wrap: wrap;
    width: 100%;
    padding-top: 6px;
    border-top: 1px solid #F1F5F9;
    margin-top: 4px;
  }
  .filters .filter-group {
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .filters .filter-label {
    font-size: 11px;
    color: #64748B;
    font-weight: 600;
  }
  .filters .chips {
    display: flex;
    gap: 4px;
    flex-wrap: wrap;
  }
  .filters .chip {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 8px;
    border-radius: 12px;
    font-size: 11px;
    border: 1px solid #CBD5E1;
    background: white;
    color: #475569;
    cursor: pointer;
    user-select: none;
  }
  .filters .chip.active {
    background: #2563EB;
    border-color: #2563EB;
    color: white;
  }
  .filters .chip:focus-visible { outline: 2px solid #2563EB; outline-offset: 1px; }
  .filters select {
    padding: 4px 8px;
    font-size: 11px;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    background: white;
  }
  .filters #filters-reset {
    margin-left: auto;
    padding: 4px 10px;
    font-size: 11px;
    border: 1px solid #CBD5E1;
    background: white;
    color: #475569;
    border-radius: 6px;
    cursor: pointer;
  }
  .filters #filters-reset:focus-visible { outline: 2px solid #2563EB; outline-offset: 1px; }
```

- [ ] **Step 3: Расширить `focusRegion` — зум к региону + карточка**

Найти заглушку `focusRegion` из Task 6 и заменить её на версию со зумом. Заменить:

```javascript
function focusRegion(f){
  // Открываем карточку — этого достаточно как минимальное поведение.
  if(typeof showRegionCard === 'function') showRegionCard(f);
}
```

на:

```javascript
function focusRegion(f){
  // Зум к региону + открытие карточки
  const svg = d3.select("#map-svg");
  try {
    // центроид по первой точке геометрии (приближение)
    const g = f.geometry;
    let coords = [];
    if(g && g.coordinates){
      if(g.type === "Polygon") coords = g.coordinates[0] || [];
      else if(g.type === "MultiPolygon") coords = (g.coordinates[0] || [])[0] || [];
    }
    if(coords.length){
      const cx = coords.reduce((s,c) => s + (c[0]||0), 0) / coords.length;
      const cy = coords.reduce((s,c) => s + (c[1]||0), 0) / coords.length;
      // проецируем через существующую функцию project (объявлена ниже в scope)
      const [px, py] = project(cx, cy);
      svg.transition().duration(500).call(
        zoom.transform,
        d3.zoomIdentity.translate(px * -1.5, py * -1.5).scale(2.5)
      );
    }
  } catch(e){ console.warn("zoom to region failed", e); }
  // Перейти в вид «Карта», если сейчас таблица
  if(window.__setView) window.__setView('map');
  if(typeof showRegionCard === 'function') showRegionCard(f);
}
```

**Важно:** `project` и `zoom` объявлены ниже в scope `drawAll()` (строки ~984 и ~1099). Чтобы `focusRegion` мог их вызвать, он должен быть в том же scope. `focusRegion` объявлен как function declaration — поднимается (hoisting), но использует `project`/`zoom` только при вызове (после их объявления), поэтому работает корректно.

- [ ] **Step 4: Добавить JS фильтров + применение + URL hash**

Внутри `drawAll()`, после `setupViewToggle()` (Task 7), добавить новую IIFE:

```javascript
// ============================================================
//  ФИЛЬТРЫ + URL HASH
// ============================================================
const FILTERS = { levels: new Set(), network: '' };

(function setupFilters(){
  const chipsHost = document.getElementById('level-chips');
  const netSel = document.getElementById('network-filter');
  const resetBtn = document.getElementById('filters-reset');
  if(!chipsHost || !netSel) return;

  // Чипсы уровней (показываем реальные уровни из LEVELS, кроме скрытых)
  chipsHost.innerHTML = LEVELS.map(lv => `
    <button type="button" class="chip" data-level="${lv.id}" aria-pressed="false">
      <span class="swatch" style="width:8px;height:8px;border-radius:2px;background:${lv.color}"></span>
      ${esc(lv.label_short)}
    </button>
  `).join('');
  chipsHost.querySelectorAll('.chip').forEach(chip => {
    const lvId = parseInt(chip.getAttribute('data-level'), 10);
    const toggle = () => {
      if(FILTERS.levels.has(lvId)) FILTERS.levels.delete(lvId);
      else FILTERS.levels.add(lvId);
      chip.classList.toggle('active', FILTERS.levels.has(lvId));
      chip.setAttribute('aria-pressed', String(FILTERS.levels.has(lvId)));
      applyFilters();
    };
    chip.addEventListener('click', toggle);
  });

  // Список сетей АЗС из truck_limits всех регионов
  const nets = new Set();
  FEATURES.forEach(f => (f.truck_limits || []).forEach(t => {
    if(t && t.network && t.network !== 'все сети') nets.add(t.network);
  }));
  [...nets].sort((a,b) => a.localeCompare(b, 'ru')).forEach(n => {
    const o = document.createElement('option');
    o.value = n; o.textContent = n;
    netSel.appendChild(o);
  });
  netSel.addEventListener('change', () => {
    FILTERS.network = netSel.value;
    applyFilters();
  });

  if(resetBtn){
    resetBtn.addEventListener('click', () => {
      FILTERS.levels.clear();
      FILTERS.network = '';
      chipsHost.querySelectorAll('.chip').forEach(c => {
        c.classList.remove('active'); c.setAttribute('aria-pressed','false');
      });
      netSel.value = '';
      const search = document.getElementById('region-search');
      if(search){ search.value = ''; const sc = document.getElementById('search-clear'); if(sc) sc.hidden = true; }
      applyFilters();
    });
  }

  // Восстановление состояния из URL hash при загрузке
  loadHashState();
})();

function getFilteredFeatures(){
  // Возвращает FEATURES после применения фильтров
  return FEATURES.filter(f => {
    if(FILTERS.levels.size > 0 && !FILTERS.levels.has(f.level)) return false;
    if(FILTERS.network){
      const has = (f.truck_limits || []).some(t => t && t.network === FILTERS.network);
      if(!has) return false;
    }
    return true;
  });
}

function applyFilters(){
  const filtered = getFilteredFeatures();
  window.__filteredFeatures = filtered;

  // Карта: затемнить отфильтрованные
  const isMap = !window.__currentView || window.__currentView() === 'map';
  const ids = new Set(filtered.map(f => f.region));
  g.selectAll("path.region").attr("opacity", d => ids.has(d.region) ? 1 : 0.25);

  // Таблица: перерисовать
  if(window.__currentView && window.__currentView() === 'table'){
    renderTable();
  }
  saveHashState();
}

function saveHashState(){
  const parts = [];
  const view = window.__currentView ? window.__currentView() : 'map';
  if(view === 'table') parts.push('view=table');
  if(FILTERS.levels.size > 0){
    parts.push('lvl=' + [...FILTERS.levels].sort().join(','));
  }
  if(FILTERS.network) parts.push('net=' + encodeURIComponent(FILTERS.network));
  const search = document.getElementById('region-search');
  if(search && search.value) parts.push('q=' + encodeURIComponent(search.value));
  const hash = parts.length ? '#' + parts.join(';') : '';
  if(location.hash !== hash){
    history.replaceState(null, '', hash || location.pathname);
  }
}

function loadHashState(){
  if(!location.hash) return;
  const params = {};
  location.hash.slice(1).split(';').forEach(p => {
    const [k, v] = p.split('=');
    if(k) params[k] = v || '';
  });
  if(params.view === 'table' && window.__setView) window.__setView('table');
  if(params.lvl){
    params.lvl.split(',').forEach(s => {
      const n = parseInt(s, 10);
      if(!isNaN(n)){
        FILTERS.levels.add(n);
        const chip = document.querySelector('.chip[data-level="' + n + '"]');
        if(chip){ chip.classList.add('active'); chip.setAttribute('aria-pressed','true'); }
      }
    });
  }
  if(params.net){
    FILTERS.network = decodeURIComponent(params.net);
    const netSel = document.getElementById('network-filter');
    if(netSel) netSel.value = FILTERS.network;
  }
  if(params.q){
    const search = document.getElementById('region-search');
    if(search){ search.value = decodeURIComponent(params.q); const sc = document.getElementById('search-clear'); if(sc) sc.hidden = false; }
  }
  applyFilters();
}
```

- [ ] **Step 5: Проверить в браузере (мок)**

Мок из Task 6 + добавить в один регион `truck_limits`, чтобы проверить фильтр по сети:
```javascript
const d = { updated: "06.07.2026", changelog: "тест", regions: [
  { region: "Москва", level: 3, price: 68.45, price_spark: [], limit_text: "60 л", truck_limits: [{network:"Лукойл", limit:"40 л"}] },
  { region: "Республика Татарстан", level: 1, price: 65.2, price_spark: [], limit_text: "—", truck_limits: [{network:"Газпромнефть", limit:"без лимита"}] },
  { region: "Чукотский АО", level: -1, price: null, price_spark: [], limit_text: "Нет данных", truck_limits: [] }
]};
```
Проверки:
1. Кликнуть чипс «Жёсткие» → на карте видна только Москва (остальные затемнены), счетчик «1 из 3».
2. В таблице (вид Таблица) после клика «Жёсткие» — 1 строка.
3. Выбрать «Лукойл» в dropdown → только Москва.
4. URL меняется на `#lvl=3;net=Лукойл`.
5. Перезагрузить страницу с этим URL → фильтр восстанавливается.
6. Кликнуть «Сбросить» → всё сбрасывается, hash очищается.
7. Ввести «татар» в поиск + Enter → карта зумится к Татарстану (если мок-геометрия позволяет) + карточка.

Expected: все 7 проверок проходят.

- [ ] **Step 6: Закоммитить**

```bash
git add index.html
git commit -m "feat: фильтры (уровень+сеть) + URL hash + зум к региону"
```

---

### Task 9: Документация — `CRONS.md` и `README.md`

**Files:**
- Modify: `CRONS.md`
- Modify: `README.md`

- [ ] **Step 1: Обновить `CRONS.md` — шаг 6 крона `diesel-heatmap-daily`**

В `CRONS.md` найти раздел **Step 6: Regenerate site data** (строки ~106-111). Заменить:

```markdown
**Step 6: Regenerate site data**

```bash
python3 /root/diesel_limits/dump_data_json.py
```

This reads the SQLite DB → produces `/srv/static/data.json` (used by the interactive map frontend) and copies `index.html` from the repo.
```

на:

```markdown
**Step 6: Regenerate site data**

```bash
python3 /root/diesel_limits/dump_data_json.py
python3 /root/diesel_limits/dump_history.py
```

`dump_data_json.py` reads the SQLite DB → produces `/srv/static/data.json` (with `price_spark` per region for sparklines) and copies `index.html` from the repo.

`dump_history.py` writes `/srv/static/history/<region>.json` for each region — price history (90 days) and limit change timeline, lazy-loaded by the region card.
```

- [ ] **Step 2: Обновить `README.md` — раздел «Что показывает карта»**

В `README.md` найти блок «По клику на регион — карточка с:» (строки ~19-23). Заменить:

```markdown
По клику на регион — карточка с:
- ценой ДТ (руб/л) и изменением за неделю
- текстом ограничений
- блоком «Для грузовиков»: лимиты по сетям АЗС (Газпромнефть, Лукойл, Роснефть, Татнефть и др.)
```

на:

```markdown
По клику на регион — карточка с:
- ценой ДТ (руб/л) и изменением за неделю
- спарклайном цены за 30 дней (тренд, min/max/среднее)
- текстом ограничений
- блоком «Для грузовиков»: лимиты по сетям АЗС (Газпромнефть, Лукойл, Роснефть, Татнефть и др.)
- блоком «История изменений»: таймлайн изменений лимитов (ужесточение ▼ / послабление ▲ / новое)
```

Затем найти блок «Справа — оперативные блоки:» (строки ~25-28) и добавить перед ним новый абзац:

```markdown
В шапке — строка управления:
- **Поиск региона** — с автодополнением, зумит карту к региону и открывает карточку
- **Переключатель Карта / Таблица** — таблица 85 регионов с сортировкой по колонкам
- **Фильтры** — по уровню ограничений и по сети АЗС; состояние сохраняется в URL

Справа — оперативные блоки:
```

- [ ] **Step 3: Закоммитить**

```bash
git add CRONS.md README.md
git commit -m "docs: описание новых функций (динамика, поиск, таблица, фильтры)"
```

---

## Self-Review

**1. Spec coverage:**
- §1 Архитектура данных (`price_spark` + lazy history) → Task 1 (spark.py), Task 2 (dump_data_json), Task 3 (dump_history). ✓
- §2 Графики динамики: спарклайн → Task 4; таймлайн (без большого графика) → Task 5. ✓
- §3 Поиск + таблица + фильтры: поиск → Task 6; таблица → Task 7; фильтры (уровень + сеть, без цен) + URL hash + зум → Task 8. ✓
- §4 Структура файлов — все 5 файлов покрыты (spark.py, dump_data_json.py, dump_history.py, index.html, CRONS.md, README.md). ✓
- §6 a11y — `aria-pressed`, `aria-live`, `:focus-visible`, `scope="col"`, tabindex на строках/заголовках → встроены в Task 6/7/8. ✓

**2. Placeholder scan:** Поиск «TBD», «TODO», «implement later», «add appropriate» — не найдено. Все шаги содержат конкретный код. ✓

**3. Type consistency:**
- `build_price_spark(rows, days=30, max_points=12) -> list[float]` — используется одинаково в Task 1 (определение) и Task 2 (вызов `build_price_spark(spark_rows)`). ✓
- `build_history(region, prices_rows, limits_rows) -> dict` — Task 1 (определение) и Task 3 (вызов в `collect_for_region`). ✓
- `price_spark` (JS) — Task 2 (добавление в data.json), Task 4 (чтение `data.price_spark`), Task 1 Step 4 Step (рендер). ✓
- `window.__filteredFeatures`, `window.__setView`, `window.__currentView` — Task 7 определяет, Task 8 потребляет. ✓
- `focusRegion` — Task 6 (заглушка), Task 8 (расширение со зумом). ✓
- `renderTable` — Task 7 определяет, Task 8 вызывает в `applyFilters`. ✓
- Имена полей истории `{"date","network","old","new"}` — Task 1 `build_history` produces, Task 3 (dump_history), Task 5 `renderTimeline` consumes — согласованы. ✓

**4. Ambiguity:** Порядок объявления `focusRegion` (Task 6) и его расширение (Task 8) — явно оговорено, что function declaration поднимается и использует `project`/`zoom` только при вызове. ✓
