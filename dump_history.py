#!/usr/bin/env python3
"""Генерирует каталог /srv/static/history/<region>.json — по файлу на регион.

Каждый файл: {"region", "prices": [...], "limits": [...]}.
Запускается после dump_data_json.py в кроне diesel-heatmap-daily.
"""
import sqlite3
import os
import sys
import json
import urllib.parse
from datetime import datetime

# Импортируем из соседних модулей репозитория
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spark import build_history
from dump_data_json import normalize_region

DB = "/root/diesel_limits/restrictions.db"
OUT_DIR = "/srv/static/history"


def collect_for_region(db, raw_region, display_region=None):
    """Собирает объект истории одного региона из БД.

    db: открытое sqlite3-подключение.
    raw_region: имя региона КАК ОНО ХРАНИТСЯ в БД (используется для SQL-фильтра).
    display_region: нормализованное имя для выходного поля region и имени файла.
                    Если None — берётся normalize_region(raw_region).

    Возвращает dict, готовый для json.dump.
    """
    display = display_region or normalize_region(raw_region)
    prices_rows = db.execute(
        "SELECT date, price FROM prices_history WHERE region=? ORDER BY date",
        (raw_region,),
    ).fetchall()
    limits_rows = db.execute(
        "SELECT source_date, network, previous_value, limit_value "
        "FROM restrictions WHERE region=? AND source_date IS NOT NULL "
        "ORDER BY source_date DESC",
        (raw_region,),
    ).fetchall()
    return build_history(display, prices_rows, limits_rows)


def write_all(db, out_dir):
    """Пишет по файлу <region>.json на каждый регион с актуальными ограничениями.

    Имя файла = urllib.parse.quote(normalized_region, safe='') + '.json'.
    SQL-запросы используют СЫРОЕ имя региона из БД (крон вставляет alias-формы
    вроде 'Адыгея', 'ХМАО'); нормализация применяется только к выходному полю
    region и имени файла. Создаёт out_dir при отсутствии.
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
        # collect_for_region опрашивает БД по сырому имени, выводит по нормализованному
        data = collect_for_region(db, raw, display_region=name)
        fname = urllib.parse.quote(name, safe="") + ".json"
        path = os.path.join(out_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        os.chmod(path, 0o644)


def main():
    db = sqlite3.connect(DB)
    # ponytail: create prices_history if missing, seed from prices
    db.execute("CREATE TABLE IF NOT EXISTS prices_history (region TEXT, date TEXT, price REAL)")
    if not db.execute("SELECT COUNT(*) FROM prices_history").fetchone()[0]:
        today = datetime.now().strftime("%Y-%m-%d")
        for r in db.execute("SELECT region, price FROM prices WHERE price IS NOT NULL"):
            db.execute("INSERT OR IGNORE INTO prices_history(region,date,price) VALUES(?,?,?)", (r[0], today, float(r[1])))
        db.commit()
        print(f"  seeded prices_history: {db.execute('SELECT COUNT(*) FROM prices_history').fetchone()[0]} rows")
    try:
        write_all(db, OUT_DIR)
    finally:
        db.close()
    # Подсчёт для лога крона
    n = len([f for f in os.listdir(OUT_DIR) if f.endswith(".json")]) if os.path.isdir(OUT_DIR) else 0
    print(f"dump_history: {n} region files written to {OUT_DIR}")


if __name__ == "__main__":
    main()
