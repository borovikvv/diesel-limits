import sqlite3
db = sqlite3.connect('/root/diesel_limits/restrictions.db')

# Цены из Росстата (13 июля 2026) и обновлённые данные
# https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html
prices = [
    ('Москва', 81.05, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Санкт-Петербург', 80.58, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Республика Адыгея', 81.30, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Республика Башкортостан', 77.75, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Республика Бурятия', 85.71, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Республика Алтай', 93.19, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Республика Дагестан', 100.49, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Республика Ингушетия', 78.11, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Кабардино-Балкарская Республика', 98.26, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Республика Калмыкия', 108.94, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Карачаево-Черкесская Республика', 75.39, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Республика Карелия', 86.96, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Республика Коми', 93.48, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Республика Марий Эл', 90.77, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Республика Мордовия', 80.63, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Республика Саха (Якутия)', 99.86, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Республика Северная Осетия — Алания', 78.32, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Республика Татарстан', 81.65, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Республика Тыва', 122.86, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Удмуртская Республика', 78.97, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Республика Хакасия', 97.43, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Чеченская Республика', 99.72, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Чувашская Республика', 85.09, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Алтайский край', 87.87, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Краснодарский край', 83.66, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Красноярский край', 91.42, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Приморский край', 92.18, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Ставропольский край', 91.26, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Хабаровский край', 88.59, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Амурская область', 92.19, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Архангельская область', 83.83, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Астраханская область', 79.39, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Белгородская область', 77.12, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Брянская область', 81.81, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Владимирская область', 89.99, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Волгоградская область', 78.15, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Вологодская область', 91.94, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Воронежская область', 97.28, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Еврейская АО', 90.73, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Забайкальский край', 97.42, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Ивановская область', 83.81, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Иркутская область', 92.97, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Калининградская область', 84.06, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Калужская область', 84.58, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Камчатский край', 106.78, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Кемеровская область', 86.64, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Кировская область', 84.36, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Костромская область', 96.77, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Курганская область', 82.55, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Курская область', 84.37, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Ленинградская область', 83.38, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Липецкая область', 86.18, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Магаданская область', 116.37, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Московская область', 83.53, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Мурманская область', 88.72, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Ненецкий АО', 87.78, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Нижегородская область', 82.50, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Новгородская область', 80.56, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Новосибирская область', 93.17, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Омская область', 79.30, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Оренбургская область', 79.47, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Орловская область', 77.22, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Пензенская область', 81.14, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Пермский край', 89.44, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Псковская область', 80.65, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Ростовская область', 81.92, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Рязанская область', 86.68, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Самарская область', 87.46, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Саратовская область', 87.51, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Сахалинская область', 100.31, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Свердловская область', 86.08, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Севастополь', 218.44, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Смоленская область', 80.84, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Тамбовская область', 92.72, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Тверская область', 82.18, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Томская область', 90.82, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Тульская область', 92.57, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Тюменская область', 95.99, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Ульяновская область', 78.65, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Ханты-Мансийский АО — Югра', 97.21, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Челябинская область', 80.65, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Чукотский АО', 78.00, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Ямало-Ненецкий АО', 83.37, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Ярославская область', 78.07, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
    ('Республика Крым', 186.20, 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html', '2026-07-13'),
]

for region, price, url, date in prices:
    db.execute('INSERT OR REPLACE INTO prices(region,price,source_url,source_date,updated_at) VALUES(?,?,?,?,datetime("now"))',
               (region, price, url, date))
db.commit()
print(f'Inserted {len(prices)} prices')

# Insert history
today = '2026-09-01'
for region, price, url, date in prices:
    db.execute('INSERT OR IGNORE INTO prices_history(region,date,price) VALUES(?,?,?)',
               (region, today, price))
db.commit()
print(f'Inserted history for {len(prices)} regions')

db.close()
