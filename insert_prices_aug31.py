import sqlite3
from datetime import datetime

# Новые цены ДТ на 31 августа 2026 (petrolplus.ru + benzup.ru)
prices_data = [
    ("Республика Адыгея", 77.71, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Республика Башкортостан", 78.15, "https://benzup.ru/index-region", "2026-08-31"),
    ("Республика Бурятия", 85.68, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Республика Алтай", 99.9, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Республика Дагестан", 105.0, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Республика Ингушетия", 76.5, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Кабардино-Балкарская Республика", 76.35, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Республика Калмыкия", 76.9, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Карачаево-Черкесская Республика", 75.15, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Республика Карелия", 84.85, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Республика Коми", 81.49, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Республика Марий Эл", 82.0, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Республика Мордовия", 78.75, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Республика Саха (Якутия)", 110.1, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Республика Северная Осетия — Алания", 74.85, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Республика Татарстан", 78.9, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Республика Тыва", 96.0, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Удмуртская Республика", 79.85, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Республика Хакасия", 95.0, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Чеченская Республика", 75.0, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Чувашская Республика", 78.84, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Алтайский край", 81.2, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Краснодарский край", 77.2, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Красноярский край", 98.13, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Приморский край", 89.22, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Ставропольский край", 77.5, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Хабаровский край", 89.04, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Амурская область", 90.18, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Архангельская область", 83.5, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Астраханская область", 77.25, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Белгородская область", 77.25, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Брянская область", 75.85, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Владимирская область", 78.55, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Волгоградская область", 77.83, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Вологодская область", 85.43, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Воронежская область", 77.1, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Еврейская АО", 89.92, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Забайкальский край", 99.7, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Ивановская область", 77.0, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Иркутская область", 87.55, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Калининградская область", 83.0, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Калужская область", 77.19, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Камчатский край", 97.15, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Кемеровская область", 80.49, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Кировская область", 93.0, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Костромская область", 79.29, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Курганская область", 80.6, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Курская область", 77.25, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Ленинградская область", 80.78, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Липецкая область", 76.15, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Магаданская область", 125.87, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Москва", 80.15, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Московская область", 78.95, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Мурманская область", 88.7, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Ненецкий АО", 86.6, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Нижегородская область", 78.2, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Новгородская область", 80.79, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Новосибирская область", 84.5, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Омская область", 79.53, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Оренбургская область", 80.0, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Орловская область", 75.8, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Пензенская область", 78.35, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Пермский край", 82.4, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Псковская область", 81.5, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Ростовская область", 77.35, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Рязанская область", 76.9, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Самарская область", 80.0, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Саратовская область", 78.15, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Сахалинская область", 96.46, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Свердловская область", 80.46, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Севастополь", 153.17, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Смоленская область", 77.4, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Тамбовская область", 76.15, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Тверская область", 80.0, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Томская область", 83.5, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Тульская область", 77.35, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Тюменская область", 81.36, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Ульяновская область", 77.45, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Ханты-Мансийский АО — Югра", 88.09, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Челябинская область", 80.5, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Чукотский АО", 78.0, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Ямало-Ненецкий АО", 84.47, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Ярославская область", 78.28, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
    ("Республика Крым", 129.63, "https://www.petrolplus.ru/fuelindex/", "2026-08-31"),
]

db = sqlite3.connect('/root/diesel_limits/restrictions.db')
inserted = 0
for region, price, url, date in prices_data:
    try:
        db.execute('INSERT OR REPLACE INTO prices(region,price,source_url,source_date,updated_at) VALUES(?,?,?,?,datetime("now"))',
                   (region, price, url, date))
        inserted += 1
    except Exception as e:
        print(f"Error {region}: {e}")

db.commit()
print(f"Inserted {inserted} prices")

# History
today = "2026-08-31"
hist = 0
for r in db.execute('SELECT region, price FROM prices WHERE price IS NOT NULL'):
    try:
        db.execute('INSERT OR IGNORE INTO prices_history(region,date,price) VALUES(?,?,?)',
                   (r[0], today, float(r[1])))
        hist += 1
    except:
        pass

db.commit()
print(f"History records: {hist}")
db.close()
