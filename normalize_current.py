#!/usr/bin/env python3
"""
Нормализует is_current в restrictions.db.

Логика:
  - Для каждого региона + сети + типа клиента помечаем is_current=1
    у записи с самой поздней source_date.
  - NULL в network / client_type приравниваем к пустой строке для группировки.
  - source_date приводим к единому формату для корректного сравнения.
  - Все остальные записи → is_current=0.

Запускать после каждой вставки новых данных.
"""
import sqlite3
from datetime import datetime

DB = "/root/diesel_limits/restrictions.db"


def normalize_date(val):
    """Приводит дату к виду YYYY-MM-DD для сравнения."""
    if not val:
        return "2000-01-01"
    val = val.strip()
    for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%Y.%m.%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(val, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return val  # если не распарсили — оставляем как есть


def main():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row

    # Читаем все записи
    rows = db.execute(
        "SELECT id, region, network, client_type, source_date FROM restrictions"
    ).fetchall()

    # Группируем: для каждого региона+сети+клиента находим запись с макс source_date
    # network=NULL и client_type=NULL приравниваем к пустой строке для группировки
    groups = {}  # (region, net, client) -> (max_date_norm, rowid)
    for r in rows:
        region = r["region"] or ""
        net = r["network"] or ""
        client = r["client_type"] or ""
        key = (region, net, client)
        date_norm = normalize_date(r["source_date"])
        if key not in groups or date_norm > groups[key][0]:
            groups[key] = (date_norm, r["id"])
        elif date_norm == groups[key][0]:
            # Если даты одинаковые — оставляем запись с бОльшим id (позже вставлена)
            if r["id"] > groups[key][1]:
                groups[key] = (date_norm, r["id"])

    current_ids = {v[1] for v in groups.values()}

    # Сначала все → 0
    db.execute("UPDATE restrictions SET is_current = 0")
    # Потом выбранные → 1
    for rid in current_ids:
        db.execute("UPDATE restrictions SET is_current = 1 WHERE id = ?", (rid,))
    db.commit()

    # Статистика
    cur = db.execute("SELECT is_current, COUNT(*) FROM restrictions GROUP BY is_current")
    stats = dict(cur.fetchall())
    total = sum(stats.values())
    print(f"Нормализация is_current: {total} записей")
    print(f"  is_current=1 (актуальные): {stats.get(1, 0)}")
    print(f"  is_current=0 (устаревшие): {stats.get(0, 0)}")

    cur = db.execute("SELECT DISTINCT region FROM restrictions WHERE is_current=1 ORDER BY region")
    regions = [r[0] for r in cur.fetchall()]
    print(f"  Регионов с актуальными данными: {len(regions)}")
    for r in regions:
        print(f"    {r}")

    db.close()


if __name__ == "__main__":
    main()
