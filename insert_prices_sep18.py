#!/usr/bin/env python3
"""Вставка свежих цен дизеля на 18 сентября 2026"""
import sqlite3
from datetime import datetime

# Цены из sravni.ru (3 августа 2026) и petrolplus.ru (свежие данные)
prices = [
    ("Санкт-Петербург", 81.17, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Алтайский край", 90.97, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Астраханская область", 80.09, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Белгородская область", 78.57, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Брянская область", 80.78, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Владимирская область", 82.70, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Волгоградская область", 80.42, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Вологодская область", 86.87, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Воронежская область", 84.58, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Еврейская АО", 90.30, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Ивановская область", 80.76, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Иркутская область", 87.27, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Кабардино-Балкарская Республика", 82.26, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Калининградская область", 84.74, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Калужская область", 78.18, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Карачаево-Черкесская Республика", 78.73, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Кемеровская область", 89.22, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Кировская область", 87.16, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Костромская область", 83.50, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Курская область", 86.29, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Ленинградская область", 83.99, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Липецкая область", 81.94, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Ненецкий АО", 87.43, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Нижегородская область", 80.33, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Оренбургская область", 81.68, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Орловская область", 76.95, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Пензенская область", 81.81, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Пермский край", 87.67, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Псковская область", 81.84, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Республика Алтай", 97.30, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Республика Тыва", 113.50, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Ростовская область", 84.61, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Рязанская область", 82.14, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Саратовская область", 84.37, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Сахалинская область", 96.53, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Свердловская область", 86.00, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Смоленская область", 80.48, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Ставропольский край", 84.88, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Тамбовская область", 85.91, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Тверская область", 81.93, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Томская область", 88.28, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Тульская область", 83.77, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Тюменская область", 94.44, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Ульяновская область", 84.09, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Ханты-Мансийский АО — Югра", 97.42, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Чеченская Республика", 79.40, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Чувашская Республика", 83.91, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Чукотский АО", 85.00, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Ямало-Ненецкий АО", 82.57, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    ("Ярославская область", 79.70, "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-03"),
    # Дополнительные данные из petrolplus.ru
    ("Краснодарский край", 77.2, "https://www.petrolplus.ru/fuelindex/", "2026-09-18"),
    ("Республика Дагестан", 105.0, "https://www.petrolplus.ru/fuelindex/", "2026-09-18"),
    ("Республика Саха (Якутия)", 110.1, "https://www.petrolplus.ru/fuelindex/", "2026-09-18"),
    ("Хабаровский край", 89.04, "https://www.petrolplus.ru/fuelindex/", "2026-09-18"),
]

db = sqlite3.connect('/root/diesel_limits/restrictions.db')
inserted = 0

for region, price, source_url, source_date in prices:
    db.execute('''INSERT OR REPLACE INTO prices (region, price, source_url, source_date, updated_at)
                 VALUES (?, ?, ?, ?, datetime('now'))''', (region, price, source_url, source_date))
    inserted += 1

db.commit()
db.close()

print(f"✅ Вставлено/обновлено: {inserted}")
print(f"📊 Всего регионов с ценами: {len(prices)}")
