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
