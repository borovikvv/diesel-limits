#!/usr/bin/env python3
"""Save fresh diesel restrictions from 29 Aug 2026 search. Ponytail: one-shot."""
import sqlite3
from datetime import datetime

DB = '/root/diesel_limits/restrictions.db'
TODAY = datetime.now().strftime('%Y-%m-%d')

# Fresh diesel restrictions found 29 Aug 2026
# Only diesel-specific or updated restrictions
restrictions = [
    # (region, city, network, client_type, limit_type, value, url, date, is_current)
    ("Астраханская область", None, "Лукойл, Газпром", "все", "объем", "40л бензина, 60л дизеля город/200л трасса", "https://www.sravni.ru/novost/2026/8/25/", "2026-08-13", 1),
    ("Крым", None, "все", "все", "объем+QR", "20л бензина, 40л дизеля, по QR-кодам", "https://www.sravni.ru/novost/2026/8/25/", "2026-08-11", 1),
    ("Севастополь", None, "все", "все", "объем+QR", "20л бензина, 40л дизеля, по QR-кодам", "https://www.sravni.ru/novost/2026/8/25/", "2026-08-11", 1),
    ("Магаданская область", "Магадан", "все", "все", "объем", "500л дизеля в Магадане, 250л в области", "https://prim.rbc.ru/prim/13/07/2026/6a5456e09a7947c742a14001", "2026-08-01", 1),
    ("Новгородская область", None, "все", "все", "запрет возраста", "с 01.09.2026 запрет продажи топлива лицам младше 18 лет", "https://www.sravni.ru/novost/2026/8/25/", "2026-08-25", 1),
    ("Новосибирская область", None, "все", "все", "объем+запрет возраста", "30л бензина, 60л дизеля; с 01.09 запрет продажи лицам младше 18", "https://www.sravni.ru/novost/2026/8/25/", "2026-08-25", 1),
    ("Калужская область", None, "все", "все", "чёт-нечет", "чёт/нечет по номерам, на дизель НЕ распространяется", "https://auto.rambler.ru/navigator/56958769/", "2026-08-15", 1),
    ("Липецкая область", None, "все", "все", "чёт-нечет", "чёт/нечет по номерам, на дизель НЕ распространяется", "https://www.sravni.ru/novost/2026/8/25/", "2026-08-13", 1),
    ("Карелия", None, "все", "все", "объем", "60л дизеля, 250л для большегрузов и спецтехники, мин 10л", "https://www.sravni.ru/novost/2026/8/25/", "2026-08-25", 1),
    ("Белгородская область", None, "все", "все", "объем", "30л бензина, 60л дизеля; запрет в канистры кроме приграничных", "https://www.sravni.ru/novost/2026/8/25/", "2026-08-21", 1),
    ("Москва", None, "Газпромнефть", "все", "объем", "до 60л дизеля город, до 200л трасса", "https://www.rbc.ru/economics/19/08/2026/6a84bb959a7947c0ad9b886f", "2026-08-19", 1),
    ("Москва", None, "Татнефть", "все", "объем", "до 60л дизеля", "https://www.rbc.ru/economics/19/08/2026/6a84bb959a7947c0ad9b886f", "2026-08-19", 1),
    ("Республика Алтай", None, "все", "все", "объем+система контроля", "50л бензина, 100л дизеля в сутки; до 01.09.2026", "https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/", "2026-08-19", 1),
    ("Волгоградская область", None, "Лукойл, Газпром", "все", "объем", "40л бензина; 60л дизеля город, 200л трасса", "https://www.sravni.ru/novost/2026/8/25/", "2026-08-25", 1),
    ("Якутия", "Якутск", "Саханефтегазсбыт", "все", "объем", "20л бензина, 50-200л дизеля; только в бак", "https://www.svoboda.org/a/denj-otstoyatj-chtoby-tretj-baka-zalitj-v-rossii-snova-defitsit-benzina/33837614.html", "2026-08-26", 1),
]

db = sqlite3.connect(DB)
# Schema: region, city, network, client_type, limit_type, value, source_url, source_date, is_current, previous_value, previous_date, inserted_at
n_new = 0
for r in restrictions:
    region, city, network, client, ltype, value, url, date, is_current = r
    db.execute('''INSERT INTO restrictions 
        (region, city, network, client_type, limit_type, value, source_url, source_date, is_current, inserted_at)
        VALUES (?,?,?,?,?,?,?,?,?,?)''',
        (region, city, network, client, ltype, value, url, date, is_current, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    n_new += 1

db.commit()
new_total = db.execute('SELECT COUNT(*) FROM restrictions').fetchone()[0]
new_active = db.execute('SELECT COUNT(*) FROM restrictions WHERE is_current=1').fetchone()[0]
db.close()
print(f"Inserted {n_new} new restrictions. Total: {new_total}, active: {new_active}")
