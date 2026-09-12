#!/usr/bin/env python3
"""Update prices and history. Ponytail."""
import sqlite3
db = sqlite3.connect('/root/diesel_limits/restrictions.db')

# 1. Show current state
print("=== PRICES COUNT ===")
print(db.execute("SELECT COUNT(*) FROM prices").fetchone()[0])
print("=== ACTIVE RESTRICTIONS ===")
print(db.execute("SELECT COUNT(*) FROM restrictions WHERE is_current=1").fetchone()[0])
print("=== TOTAL RESTRICTIONS ===")
print(db.execute("SELECT COUNT(*) FROM restrictions").fetchone()[0])
print("=== HISTORY COUNT ===")
print(db.execute("SELECT COUNT(*) FROM prices_history").fetchone()[0])

# 2. Fresh prices from petrolplus.ru (Sep 5, 2026)
# Extracted DТ prices per region
url = "https://www.petrolplus.ru/fuelindex/"
date_str = "2026-09-05"

prices_new = {
    "Москва": 80.15, "Санкт-Петербург": 80.65, "Алтайский край": 81.2,
    "Амурская область": 90.18, "Архангельская область": 83.5,
    "Астраханская область": 77.55, "Белгородская область": 77.25,
    "Брянская область": 75.85, "Владимирская область": 78.55,
    "Волгоградская область": 78.93, "Вологодская область": 84.93,
    "Воронежская область": 77.1, "Еврейская АО": 89.92,
    "Забайкальский край": 99.9, "Ивановская область": 77.0,
    "Иркутская область": 88.0, "Кабардино-Балкарская Республика": 76.35,
    "Калининградская область": 83.0, "Калужская область": 77.24,
    "Камчатский край": 97.15, "Карачаево-Черкесская Республика": 75.15,
    "Кемеровская область": 80.49, "Кировская область": 93.0,
    "Костромская область": 79.29, "Краснодарский край": 77.2,
    "Красноярский край": 99.5, "Курганская область": 80.6,
    "Курская область": 77.25, "Ленинградская область": 80.95,
    "Липецкая область": 76.15, "Московская область": 78.99,
    "Мурманская область": 88.7, "Ненецкий АО": 86.6,
    "Нижегородская область": 78.83, "Новгородская область": 80.79,
    "Новосибирская область": 84.3, "Омская область": 79.53,
    "Оренбургская область": 80.0, "Орловская область": 75.8,
    "Пензенская область": 78.35, "Пермский край": 82.4,
    "Приморский край": 89.37, "Псковская область": 81.5,
    "Республика Адыгея": 77.71, "Республика Алтай": 99.9,
    "Республика Башкортостан": 78.15, "Республика Бурятия": 85.75,
    "Республика Дагестан": 105.0, "Республика Ингушетия": 76.5,
    "Республика Калмыкия": 77.2, "Республика Карелия": 84.13,
    "Республика Коми": 81.49, "Республика Марий Эл": 82.83,
    "Республика Мордовия": 78.75, "Республика Саха (Якутия)": 111.77,
    "Республика Северная Осетия — Алания": 75.15,
    "Республика Татарстан": 78.9, "Республика Тыва": 96.0,
    "Республика Хакасия": 95.0, "Ростовская область": 77.35,
    "Рязанская область": 76.9, "Самарская область": 80.0,
    "Саратовская область": 78.15, "Сахалинская область": 96.46,
    "Свердловская область": 80.49, "Смоленская область": 77.4,
    "Ставропольский край": 77.5, "Тамбовская область": 76.15,
    "Тверская область": 80.0, "Томская область": 83.5,
    "Тульская область": 77.35, "Тюменская область": 81.64,
    "Удмуртская Республика": 79.85, "Ульяновская область": 77.45,
    "Хабаровский край": 89.04, "Ханты-Мансийский АО — Югра": 88.09,
    "Челябинская область": 80.5, "Чеченская Республика": 72.0,
    "Чувашская Республика": 78.72, "Ямало-Ненецкий АО": 85.57,
    "Ярославская область": 78.23, "Республика Крым": 129.63,
    "Севастополь": 153.17, "Магаданская область": 125.87,
    "Чукотский АО": 78.0,
}

inserted = 0
for region, price in prices_new.items():
    db.execute(
        "INSERT OR REPLACE INTO prices(region,price,source_url,source_date,updated_at) VALUES(?,?,?,?,datetime('now'))",
        (region, price, url, date_str)
    )
    inserted += 1

db.commit()
print(f"\n=== PRICES INSERTED: {inserted} ===")

# 3. Insert into prices_history
today = "2026-09-06"
hist = 0
for r in db.execute("SELECT region, price FROM prices WHERE price IS NOT NULL"):
    db.execute(
        "INSERT OR IGNORE INTO prices_history(region,date,price) VALUES(?,?,?)",
        (r[0], today, float(r[1]))
    )
    hist += 1
db.commit()
print(f"=== HISTORY ROWS INSERTED/IGNORED: {hist} ===")

# 4. Final stats
print(f"\n=== FINAL STATS ===")
print(f"prices: {db.execute('SELECT COUNT(*) FROM prices').fetchone()[0]}")
print(f"active restrictions: {db.execute('SELECT COUNT(*) FROM restrictions WHERE is_current=1').fetchone()[0]}")
print(f"total restrictions: {db.execute('SELECT COUNT(*) FROM restrictions').fetchone()[0]}")
print(f"changes: {db.execute('SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL').fetchone()[0]}")

import os
hist_files = len(os.listdir("/srv/static/history"))
print(f"history files: {hist_files}")
print(f"total prices_history: {db.execute('SELECT COUNT(*) FROM prices_history').fetchone()[0]}")

db.close()
