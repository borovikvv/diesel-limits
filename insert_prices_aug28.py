"""Insert diesel prices from petrolplus.ru (2026-08-21) and benzup.ru (2026-08-25)"""
import sqlite3

db = sqlite3.connect('/root/diesel_limits/restrictions.db')

# Prices from petrolplus.ru - ДТ column (diesel), date 2026-08-21
petrolplus = {
    'Москва': 80.15,
    'Санкт-Петербург': 80.65,
    'Алтайский край': 81.2,
    'Амурская область': 90.18,
    'Архангельская область': 83.5,
    'Астраханская область': 77.25,
    'Белгородская область': 77.25,
    'Брянская область': 75.85,
    'Владимирская область': 78.55,
    'Волгоградская область': 79.0,
    'Вологодская область': 84.93,
    'Воронежская область': 77.1,
    'Еврейская автономная область': 89.92,
    'Забайкальский край': 99.7,
    'Ивановская область': 77.0,
    'Иркутская область': 87.55,
    'Кабардино-Балкарская Республика': 76.35,
    'Калининградская область': 83.0,
    'Калужская область': 77.19,
    'Камчатский край': 97.15,
    'Карачаево-Черкесская Республика': 75.15,
    'Кемеровская область': 80.49,
    'Кировская область': 93.0,
    'Костромская область': 79.29,
    'Краснодарский край': 77.2,
    'Красноярский край': 98.13,
    'Курганская область': 80.6,
    'Курская область': 77.25,
    'Ленинградская область': 80.78,
    'Липецкая область': 76.15,
    'Московская область': 78.95,
    'Мурманская область': 88.7,
    'Ненецкий автономный округ': 86.6,
    'Нижегородская область': 78.2,
    'Новгородская область': 80.79,
    'Новосибирская область': 84.5,
    'Омская область': 79.53,
    'Оренбургская область': 80.0,
    'Орловская область': 75.8,
    'Пензенская область': 78.35,
    'Пермский край': 82.4,
    'Приморский край': 89.22,
    'Псковская область': 81.5,
    'Республика Адыгея': 77.71,
    'Республика Алтай': 99.9,
    'Республика Башкортостан': 78.15,
    'Республика Бурятия': 85.68,
    'Республика Дагестан': 105.0,
    'Республика Ингушетия': 76.5,
    'Республика Калмыкия': 76.9,
    'Республика Карелия': 84.85,
    'Республика Коми': 81.49,
    'Республика Марий Эл': 82.0,
    'Республика Мордовия': 78.75,
    'Республика Саха (Якутия)': 110.1,
    'Республика Северная Осетия — Алания': 74.85,
    'Республика Татарстан': 78.9,
    'Республика Тыва': 96.0,
    'Республика Хакасия': 95.0,
    'Ростовская область': 77.35,
    'Рязанская область': 76.9,
    'Самарская область': 80.0,
    'Саратовская область': 78.15,
    'Сахалинская область': 96.46,
    'Свердловская область': 80.46,
    'Смоленская область': 77.4,
    'Ставропольский край': 77.5,
    'Тамбовская область': 76.15,
    'Тверская область': 80.0,
    'Томская область': 83.5,
    'Тульская область': 77.35,
    'Тюменская область': 81.36,
    'Удмуртская Республика': 79.85,
    'Ульяновская область': 77.45,
    'Хабаровский край': 89.04,
    'Ханты-Мансийский автономный округ - Югра': 88.09,
    'Челябинская область': 80.5,
    'Чеченская Республика': 75.0,
    'Чувашская Республика': 78.84,
    'Ямало-Ненецкий автономный округ': 84.47,
    'Ярославская область': 78.28,
}

URL = 'https://www.petrolplus.ru/fuelindex/'
DATE = '2026-08-21'
new_prices = 0
updated_prices = 0

for region, price in petrolplus.items():
    existing = db.execute('SELECT price FROM prices WHERE region=?', (region,)).fetchone()
    if existing:
        if abs(existing[0] - price) > 0.01:
            db.execute('UPDATE prices SET price=?, source_url=?, source_date=?, updated_at=datetime("now") WHERE region=?',
                       (price, URL, DATE, region))
            updated_prices += 1
    else:
        db.execute('INSERT INTO prices(region,price,source_url,source_date,updated_at) VALUES(?,?,?,?,datetime("now"))',
                   (region, price, URL, DATE))
        new_prices += 1

db.commit()
print(f'Prices: {new_prices} new, {updated_prices} updated')

# Now insert into prices_history for today
from datetime import date
today = date.today().isoformat()
hist_count = 0
for r in db.execute('SELECT region, price FROM prices WHERE price IS NOT NULL'):
    existing = db.execute('SELECT 1 FROM prices_history WHERE region=? AND date=?', (r[0], today)).fetchone()
    if not existing:
        db.execute('INSERT INTO prices_history(region,date,price) VALUES(?,?,?)', (r[0], today, float(r[1])))
        hist_count += 1

db.commit()
print(f'History: {hist_count} new entries for {today}')

# Stats
print(f'Total prices: {db.execute("SELECT COUNT(*) FROM prices").fetchone()[0]}')
print(f'Total history: {db.execute("SELECT COUNT(*) FROM prices_history").fetchone()[0]}')
db.close()
