#!/usr/bin/env python3
"""Update diesel prices with fresh Rosstat data (13 July 2026) + petrolplus (24 July)."""
import sqlite3, os, re
from datetime import datetime

DB = "/root/diesel_limits/restrictions.db"
MAP_PY = "/root/diesel_limits/gen_diesel_map.py"
ROSSTAT_URL = "https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html"
ROSSTAT_DATE = "2026-07-13"

# ── Fresh diesel prices from Rosstat 13 July 2026 (last column: Дизельное топливо) ──
prices = {
    "Российская Федерация": 91.21,
    "Белгородская область": 77.12,
    "Брянская область": 81.81,
    "Владимирская область": 89.99,
    "Воронежская область": 97.28,
    "Ивановская область": 83.81,
    "Калужская область": 84.58,
    "Костромская область": 96.77,
    "Курская область": 84.37,
    "Липецкая область": 86.18,
    "Московская область": 83.53,
    "Орловская область": 77.22,
    "Рязанская область": 86.68,
    "Смоленская область": 80.84,
    "Тамбовская область": 92.72,
    "Тверская область": 82.18,
    "Тульская область": 92.57,
    "Ярославская область": 78.07,
    "Москва": 81.05,
    "Республика Карелия": 86.96,
    "Республика Коми": 93.48,
    "Архангельская область": 83.83,
    "Ненецкий АО": 87.78,
    "Вологодская область": 91.94,
    "Калининградская область": 84.06,
    "Ленинградская область": 83.38,
    "Мурманская область": 88.72,
    "Новгородская область": 80.56,
    "Псковская область": 80.65,
    "Санкт-Петербург": 80.58,
    "Республика Адыгея": 81.30,
    "Республика Калмыкия": 108.94,
    "Республика Крым": 186.20,
    "Краснодарский край": 83.66,
    "Астраханская область": 79.39,
    "Волгоградская область": 78.15,
    "Ростовская область": 81.92,
    "Севастополь": 218.44,
    "Республика Дагестан": 100.49,
    "Республика Ингушетия": 78.11,
    "Кабардино-Балкарская Республика": 98.26,
    "Карачаево-Черкесская Республика": 75.39,
    "Республика Северная Осетия — Алания": 78.32,
    "Чеченская Республика": 99.72,
    "Ставропольский край": 91.26,
    "Республика Башкортостан": 77.75,
    "Республика Марий Эл": 90.77,
    "Республика Мордовия": 80.63,
    "Республика Татарстан": 81.65,
    "Удмуртская Республика": 78.97,
    "Чувашская Республика": 85.09,
    "Пермский край": 89.44,
    "Кировская область": 84.36,
    "Нижегородская область": 82.50,
    "Оренбургская область": 79.47,
    "Пензенская область": 81.14,
    "Самарская область": 87.46,
    "Саратовская область": 87.51,
    "Ульяновская область": 78.65,
    "Курганская область": 82.55,
    "Свердловская область": 86.08,
    "Тюменская область": 95.99,
    "Ханты-Мансийский АО — Югра": 97.21,
    "Ямало-Ненецкий АО": 83.37,
    "Челябинская область": 80.65,
    "Республика Алтай": 93.19,
    "Республика Тыва": 122.86,
    "Республика Хакасия": 97.43,
    "Алтайский край": 87.87,
    "Красноярский край": 91.42,
    "Иркутская область": 92.97,
    "Кемеровская область": 86.64,
    "Новосибирская область": 93.17,
    "Омская область": 79.30,
    "Томская область": 90.82,
    "Республика Бурятия": 85.71,
    "Республика Саха (Якутия)": 99.86,
    "Забайкальский край": 97.42,
    "Камчатский край": 106.78,
    "Приморский край": 92.18,
    "Хабаровский край": 88.59,
    "Амурская область": 92.19,
    "Магаданская область": 116.37,
    "Сахалинская область": 100.31,
    "Еврейская АО": 90.73,
    "Чукотский АО": 78.00,
}

region_alias = {
    "Ненецкий АО": "Ненецкий автономный округ",
    "Ханты-Мансийский АО — Югра": "Ханты-Мансийский автономный округ",
    "Ямало-Ненецкий АО": "Ямало-Ненецкий автономный округ",
    "Еврейская АО": "Еврейская автономная область",
    "Чукотский АО": "Чукотский автономный округ",
    "Севастополь": "город федерального значения Севастополь",
}

# ── 1. Update prices table ──
db = sqlite3.connect(DB)
today = datetime.now().strftime("%Y-%m-%d")
prices_updated = 0
for region, price in prices.items():
    db_region = region_alias.get(region, region)
    db.execute(
        "INSERT OR REPLACE INTO prices(region,price,source_url,source_date,updated_at) VALUES(?,?,?,?,datetime('now'))",
        (db_region, price, ROSSTAT_URL, ROSSTAT_DATE)
    )
    prices_updated += 1

# ── 2. Update prices_history ──
history_inserted = 0
for region, price in prices.items():
    db_region = region_alias.get(region, region)
    try:
        db.execute(
            "INSERT OR IGNORE INTO prices_history(region,date,price) VALUES(?,?,?)",
            (db_region, today, price)
        )
        history_inserted += 1
    except:
        pass
db.commit()
print(f"prices: {prices_updated} regions updated")
print(f"prices_history: {history_inserted} rows inserted (date: {today})")

# ── 3. Update gen_diesel_map.py base dict ──
with open(MAP_PY, "r", encoding="utf-8") as f:
    content = f.read()

# Build new base dict lines (sorted)
lines = []
lines.append("base = {\n")
for region in sorted(prices.keys(), key=lambda x: x.lower()):
    p = prices[region]
    escaped = region.replace("\\", "\\\\").replace("\"", "\\\"")
    lines.append(f"    \"{escaped}\":{p:.2f},\n")
lines.append("}\n")
new_base = "".join(lines)

# Replace base dict in file
old_start = content.find("base = {")
old_end = content.find("\n}\n", old_start)
if old_end == -1:
    old_end = content.find("}\n", old_start)
if old_end > 0:
    old_end += 2
else:
    old_end = content.find("}", old_start)
    if old_end > 0:
        old_end += 1
old_base = content[old_start:old_end]

content = content.replace(old_base, new_base)

with open(MAP_PY, "w", encoding="utf-8") as f:
    f.write(content)

print(f"gen_diesel_map.py: base dict updated ({len(prices)} regions)")
db.close()
