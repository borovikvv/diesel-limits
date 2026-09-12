import sqlite3

db = sqlite3.connect('/root/diesel_limits/restrictions.db')

# Данные с sravni.ru от 17.08.2026 (актуальные на момент поиска)
prices_data = [
    ('Алтайский край', 88.96, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Амурская область', 92.41, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Архангельская область', 85.62, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Астраханская область', 79.34, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Белгородская область', 78.18, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Брянская область', 80.11, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Владимирская область', 82.22, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Волгоградская область', 80.04, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Вологодская область', 86.20, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Воронежская область', 86.00, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Еврейская автономная область', 91.89, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Забайкальский край', 100.13, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Ивановская область', 79.34, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Иркутская область', 88.18, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Кабардино-Балкарская Республика', 81.73, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Калининградская область', 84.44, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Калужская область', 78.09, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Камчатский край', 111.97, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Карачаево-Черкесская Республика', 78.58, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Кемеровская область', 85.88, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Кировская область', 88.39, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Костромская область', 81.68, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Краснодарский край', 80.95, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Красноярский край', 97.71, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Курганская область', 82.50, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Курская область', 83.20, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Ленинградская область', 82.12, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Липецкая область', 81.85, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Магаданская область', 126.33, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Московская область', 83.51, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Мурманская область', 88.25, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Ненецкий автономный округ', 88.09, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Нижегородская область', 80.09, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Новгородская область', 80.76, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Новосибирская область', 89.07, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Омская область', 80.03, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Оренбургская область', 81.83, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Орловская область', 76.66, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Пензенская область', 82.27, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Пермский край', 86.68, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Приморский край', 93.24, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Псковская область', 81.81, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Республика Адыгея', 81.61, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Республика Алтай', 96.29, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Республика Башкортостан', 79.00, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Республика Дагестан', 96.34, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Республика Бурятия', 86.10, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Республика Ингушетия', 81.20, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Республика Калмыкия', 79.19, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Республика Карелия', 84.93, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Республика Коми', 81.81, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Республика Марий Эл', 81.27, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Республика Мордовия', 85.07, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Республика Саха (Якутия)', 110.95, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Республика Северная Осетия — Алания', 77.91, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Республика Татарстан', 80.63, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Республика Тыва', 116.32, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Республика Хакасия', 91.57, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Ростовская область', 83.41, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Рязанская область', 83.20, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Самарская область', 84.84, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Саратовская область', 83.85, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Сахалинская область', 97.32, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Свердловская область', 83.58, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Смоленская область', 80.20, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Ставропольский край', 81.37, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Тамбовская область', 85.50, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Тверская область', 81.86, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Томская область', 90.28, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Тульская область', 81.52, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Тюменская область', 89.56, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Удмуртская Республика', 81.24, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Ульяновская область', 82.21, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Хабаровский край', 94.84, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Ханты-Мансийский автономный округ', 95.88, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Челябинская область', 83.26, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Чеченская Республика', 83.95, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Чувашская Республика', 83.14, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Чукотский автономный округ', 83.33, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Ямало-Ненецкий автономный округ', 83.32, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
    ('Ярославская область', 79.55, 'https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-17'),
]

cnt = 0
for region, price, url, date in prices_data:
    db.execute('INSERT OR REPLACE INTO prices(region,price,source_url,source_date,updated_at) VALUES(?,?,?,?,datetime("now"))',
               (region, price, url, date))
    cnt += 1

db.commit()
print(f'Inserted/updated {cnt} prices')

# Add to history
today = '2026-08-20'
hcnt = 0
for region, price, _, _ in prices_data:
    db.execute('INSERT OR IGNORE INTO prices_history(region,date,price) VALUES(?,?,?)',
               (region, today, float(price)))
    hcnt += 1

db.commit()
print(f'History records: {hcnt}')
db.close()
