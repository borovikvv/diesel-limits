"""Insert/update prices from Rosstat 13 July 2026 + new restrictions."""
import sqlite3
from datetime import datetime

DB_PATH = '/root/diesel_limits/restrictions.db'
TODAY = '2026-08-07'

# ── 1. PRICES from Rosstat 13 July 2026 (дизель, ₽/л) ──
SOURCE_URL = 'https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html'
SOURCE_DATE = '2026-07-13'

rosstat = {
    "Алтайский край": 89.53, "Амурская область": 92.19, "Архангельская область": 83.83,
    "Астраханская область": 79.39, "Белгородская область": 77.12, "Брянская область": 81.81,
    "Владимирская область": 89.99, "Волгоградская область": 78.15, "Вологодская область": 91.94,
    "Воронежская область": 97.28, "Еврейская АО": 90.73, "Забайкальский край": 97.42,
    "Ивановская область": 83.81, "Иркутская область": 92.97,
    "Кабардино-Балкарская Республика": 98.26, "Калининградская область": 84.06,
    "Калужская область": 84.58, "Камчатский край": 106.78,
    "Карачаево-Черкесская Республика": 75.39, "Кемеровская область": 86.64,
    "Кировская область": 84.36, "Костромская область": 96.77, "Краснодарский край": 83.66,
    "Красноярский край": 91.42, "Курганская область": 82.55, "Курская область": 84.37,
    "Ленинградская область": 83.38, "Липецкая область": 86.18,
    "Магаданская область": 116.37, "Москва": 81.05, "Московская область": 83.53,
    "Мурманская область": 88.72, "Ненецкий АО": 87.78, "Нижегородская область": 82.50,
    "Новгородская область": 80.56, "Новосибирская область": 93.17, "Омская область": 79.30,
    "Оренбургская область": 79.47, "Орловская область": 77.22, "Пензенская область": 81.14,
    "Пермский край": 89.44, "Приморский край": 92.18, "Псковская область": 80.65,
    "Республика Адыгея": 81.30, "Республика Алтай": 93.19,
    "Республика Башкортостан": 77.75, "Республика Бурятия": 85.71,
    "Республика Дагестан": 100.49, "Республика Ингушетия": 78.11,
    "Республика Калмыкия": 108.94, "Республика Карелия": 86.96,
    "Республика Коми": 93.48, "Республика Крым": 186.20, "Республика Марий Эл": 90.77,
    "Республика Мордовия": 80.63, "Республика Саха (Якутия)": 99.86,
    "Республика Северная Осетия — Алания": 78.32, "Республика Татарстан": 81.65,
    "Республика Тыва": 122.86, "Республика Хакасия": 97.43,
    "Ростовская область": 81.92, "Рязанская область": 86.68, "Самарская область": 87.46,
    "Санкт-Петербург": 80.58, "Сахалинская область": 100.31, "Свердловская область": 86.08,
    "Севастополь": 218.44, "Смоленская область": 80.84, "Ставропольский край": 91.26,
    "Тамбовская область": 92.72, "Тверская область": 82.18, "Томская область": 90.82,
    "Тульская область": 92.57, "Тюменская область": 95.99, "Удмуртская Республика": 78.97,
    "Ульяновская область": 78.65, "Хабаровский край": 88.59,
    "Ханты-Мансийский АО — Югра": 97.21, "Челябинская область": 80.65,
    "Чеченская Республика": 99.72, "Чувашская Республика": 85.09,
    "Чукотский АО": 78.0, "Ямало-Ненецкий АО": 83.37, "Ярославская область": 78.07,
}

db = sqlite3.connect(DB_PATH)
prices_updated = 0
for region, price in rosstat.items():
    db.execute(
        'INSERT OR REPLACE INTO prices(region,price,source_url,source_date,updated_at) VALUES(?,?,?,?,datetime("now"))',
        (region, price, SOURCE_URL, SOURCE_DATE)
    )
    prices_updated += 1

# History
hist_count = 0
for region, price in rosstat.items():
    existing = db.execute('SELECT 1 FROM prices_history WHERE region=? AND date=?', (region, TODAY)).fetchone()
    if not existing:
        db.execute('INSERT INTO prices_history(region,date,price) VALUES(?,?,?)', (region, TODAY, float(price)))
        hist_count += 1

db.commit()
print(f"Prices inserted/updated: {prices_updated}")
print(f"History entries added: {hist_count}")

# ── 2. RESTRICTIONS — свежие (август 2026) ──
# Sources: lenta.ru, rbc.ru, aa.com.tr, sravni.ru — июль-август 2026

restrictions = [
    # Rostovskaya oblast — rbc.ru 10/07/2026
    ("Ростовская область", None, None, "физлица", "объем", "бензин 30л, дизель 60л; грузовые 200-300л", None,
     "https://www.rbc.ru/economics/10/07/2026/6a50e9859a7947e50d76ffd8", "2026-07-10", 1),
    
    # Magadanskaya oblast — rbc.ru 13/07/2026
    ("Магаданская область", "Магадан", None, "все", "объем", "дизель до 500л/сутки в Магадане, 250л в районе", None,
     "https://prim.rbc.ru/prim/13/07/2026/6a5456e09a7947c742a14001", "2026-07-13", 1),
    
    # Sankt-Peterburg — rbc.ru 24/06/2026
    ("Санкт-Петербург", None, "Лукойл", "физлица", "объем", "бензин 30л, дизель 60л", None,
     "https://www.rbc.ru/economics/24/06/2026/6a3c13c59a7947597979e6a3", "2026-06-24", 1),
    
    # Tatarstan — Газпромнефть
    ("Республика Татарстан", None, "Газпромнефть", "физлица", "объем", "бензин 30л, дизель 60л", None,
     "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-07-01", 1),
    
    # Krasnodarskiy kray — lente.ru 07/07/2026
    ("Краснодарский край", None, None, "физлица", "объем", "бензин 20-30л, дизель 30-60л", None,
     "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07", 1),
    
    # Primorskiy kray — lente.ru
    ("Приморский край", None, None, "грузовые", "объем", "дизель: 100л город, 200л трасса", None,
     "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07", 1),
    
    # Pskovskaya oblast — lente.ru
    ("Псковская область", None, None, "физлица", "объем", "дизель до 40л", None,
     "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-06-15", 1),
    
    # Udmurtiya — lente.ru
    ("Удмуртская Республика", None, None, "физлица", "объем", "дизель до 40л", None,
     "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-06-15", 1),
    
    # Vladimirskaya oblast — lente.ru 18/06/2026
    ("Владимирская область", None, None, "физлица", "объем", "бензин 20-30л, дизель 40л", None,
     "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-06-18", 1),
    
    # Belgorodskaya oblast — lente.ru 03/07/2026
    ("Белгородская область", None, None, "физлица", "объем", "лимиты на уровне АЗС", None,
     "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-03", 1),
    
    # Daghestan — aa.com.tr
    ("Республика Дагестан", None, None, "физлица", "объем", "бензин 20л, дизель 50л", None,
     "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-07-01", 1),
    
    # Voronezhskaya oblast — aa.com.tr
    ("Воронежская область", None, None, "физлица", "объем", "бензин 30л, дизель 60л", None,
     "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-06-24", 1),
    
    # Kaliningradskaya oblast — aa.com.tr
    ("Калининградская область", None, None, "физлица", "объем", "бензин 30л, дизель 60л", None,
     "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-06-24", 1),
    
    # Murmanskaya oblast — Lukoil
    ("Мурманская область", None, "Лукойл", "физлица", "объем", "бензин 30л, дизель 60л", None,
     "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-06-24", 1),
    
    # Omskaya oblast — aa.com.tr
    ("Омская область", None, None, "физлица", "объем", "бензин 40л, дизель 80л; трасса дизель 200л", None,
     "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-06-22", 1),
    
    # Kemerovskaya oblast — aa.com.tr
    ("Кемеровская область", None, None, "физлица", "объем", "бензин 40л, дизель 80л; трасса дизель 200л", None,
     "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-06-22", 1),
    
    # Yakutiya — aa.com.tr
    ("Республика Саха (Якутия)", None, None, "физлица", "объем", "бензин 30л, дизель 200л; запрет в переносные ёмкости", None,
     "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-06-24", 1),
    
    # Samarskaya oblast — Kommersant 24/06
    ("Самарская область", None, None, "физлица", "объем", "бензин 40л, дизель 100л (2 недели)", None,
     "https://www.kommersant.ru/doc/8764043", "2026-06-24", 1),
    
    # Kirovskaya + Ulyanovskaya — lente.ru
    ("Кировская область", None, None, "физлица", "объем", "дизель до 100л на некоторых АЗС", None,
     "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07", 1),
    
    ("Ульяновская область", None, None, "физлица", "объем", "дизель до 100л на некоторых АЗС", None,
     "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07", 1),
    
    # Adygeya — lente.ru
    ("Республика Адыгея", None, None, "все", "объем", "лимиты на АЗС; ключевые организации на дизеле", None,
     "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07", 1),
]

restr_new = 0
restr_upd = 0
for r in restrictions:
    region, city, network, client_type, limit_type, limit_value, prev_value, url, date, is_current = r
    try:
        db.execute('''INSERT INTO restrictions 
            (region, city, network, client_type, limit_type, limit_value, previous_value, source_url, source_date, is_current)
            VALUES (?,?,?,?,?,?,?,?,?,?)''',
            (region, city, network, client_type, limit_type, limit_value, prev_value, url, date, is_current))
        restr_new += 1
    except sqlite3.IntegrityError:
        # Update existing
        db.execute('''UPDATE restrictions SET limit_value=?, previous_value=COALESCE(previous_value,limit_value),
            source_url=?, source_date=?, is_current=?, updated_at=datetime("now")
            WHERE region=? AND network IS ? AND client_type=? AND limit_type=?''',
            (limit_value, url, date, is_current, region, network, client_type, limit_type))
        restr_upd += 1

db.commit()
db.close()
print(f"Restrictions: {restr_new} new, {restr_upd} updated")
