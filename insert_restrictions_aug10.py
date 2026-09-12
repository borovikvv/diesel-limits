#!/usr/bin/env python3
"""Insert fresh diesel restrictions from 10 Aug 2026 sources. Ponytail."""
import sqlite3
from datetime import datetime

db = sqlite3.connect('/root/diesel_limits/restrictions.db')

# Fresh restrictions from web search (10 Aug 2026)
# Format: (region, city, network, client_type, limit_type, limit_value, previous_value, source_url, source_date)
restrictions = [
    # Дагестан - aa.com.tr
    ('Республика Дагестан', None, None, 'все', 'объем', '20л бензин, 50л дизель', None,
     'https://www.aa.com.tr/ru/3983182', '2026-08-10'),
    # Адыгея - aa.com.tr
    ('Республика Адыгея', None, None, 'все', 'объем', '40л бензин, 60л дизель', None,
     'https://www.aa.com.tr/ru/3983182', '2026-08-10'),
    # Воронежская область
    ('Воронежская область', None, None, 'все', 'объем', '30л бензин, 60л дизель', None,
     'https://www.aa.com.tr/ru/3983182', '2026-08-10'),
    # Калининградская область - Лукойл снял лимиты с 28 июля
    ('Калининградская область', None, 'Лукойл', 'все', 'отмена', 'лимиты сняты с 28 июля', '30л бензин, 60л дизель',
     'https://auto.ru/mag/article/srazu-neskolko-regionov-rf-snyali-ryad-ogranicheniy-na-prodazhu-topliva/', '2026-08-10'),
    # Кировская область
    ('Кировская область', None, None, 'все', 'объем', '30л бензин', None,
     'https://www.aa.com.tr/ru/3983182', '2026-08-10'),
    # Мурманская область - Lukoil
    ('Мурманская область', None, 'Lukoil', 'все', 'объем', '30л бензин, 60л дизель', None,
     'https://www.aa.com.tr/ru/3983182', '2026-08-10'),
    # Омская область
    ('Омская область', None, None, 'все', 'объем', '40л бензин, 80л дизель (200л дизель на трассах)', None,
     'https://www.aa.com.tr/ru/3983182', '2026-08-10'),
    # Кемеровская область
    ('Кемеровская область', None, None, 'все', 'объем', '40л бензин, 80л дизель, 200л дизель на трассах', None,
     'https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm', '2026-08-10'),
    # Якутия
    ('Республика Саха (Якутия)', None, None, 'все', 'объем', '30л бензин, 200л дизель', None,
     'https://www.aa.com.tr/ru/3983182', '2026-08-10'),
    # Москва - Lenta.ru
    ('Москва', None, None, 'все', 'объем', '20-30л бензин, до 60л дизель, до 200л дизель на трассах', None,
     'https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm', '2026-08-10'),
    # Белгородская область - RBC
    ('Белгородская область', None, None, 'все', 'объем', '30л бензин, 60л дизель', None,
     'https://www.rbc.ru/economics/03/07/2026/6a461d589a79474020d03021', '2026-08-10'),
    # Мордовия - RBC (updated: was 20l, now 40l)
    ('Республика Мордовия', None, None, 'все', 'объем', '40л бензин', '20л бензин',
     'https://www.rbc.ru/economics/03/07/2026/6a461d589a79474020d03021', '2026-08-10'),
    # Калмыкия - RBC (updated: was 20l, now 30l)
    ('Республика Калмыкия', None, None, 'все', 'объем', '30л бензин', '20л бензин',
     'https://www.rbc.ru/economics/03/07/2026/6a461d589a79474020d03021', '2026-08-10'),
    # Новосибирская область - RBC
    ('Новосибирская область', None, None, 'все', 'объем', '30л бензин, 60л дизель', None,
     'https://www.rbc.ru/economics/03/07/2026/6a461d589a79474020d03021', '2026-08-10'),
    # Приморский край - RBC
    ('Приморский край', None, None, 'все', 'объем', 'ограничения для большегрузов, запрет в канистры', None,
     'https://www.rbc.ru/economics/03/07/2026/6a461d589a79474020d03021', '2026-08-10'),
    # Магаданская область - RBC (до сентября)
    ('Магаданская область', None, None, 'все', 'объем', '100л бензин/сутки, 500л дизель/сутки в Магадане, 250л дизель/сутки в области', None,
     'https://prim.rbc.ru/prim/13/07/2026/6a5456e09a7947c742a14001', '2026-08-10'),
    # Пензенская область - Sravni.ru
    ('Пензенская область', None, None, 'все', 'объем', '100л бензин, 200л дизель. Только в бак', None,
     'https://www.sravni.ru/novost/2026/7/28/', '2026-08-10'),
    # Тамбовская область - четные/нечетные дни
    ('Тамбовская область', None, None, 'все', 'время', 'четные/нечетные дни заправки', None,
     'https://www.rbc.ru/economics/03/07/2026/6a461d589a79474020d03021', '2026-08-10'),
    # Липецкая область - четные/нечетные дни
    ('Липецкая область', None, None, 'все', 'время', 'четные/нечетные дни заправки', None,
     'https://www.rbc.ru/economics/03/07/2026/6a461d589a79474020d03021', '2026-08-10'),
    # Астраханская область - четные/нечетные дни
    ('Астраханская область', None, None, 'все', 'время', 'заправка по четным/нечетным дням', None,
     'https://www.rbc.ru/economics/03/07/2026/6a461d589a79474020d03021', '2026-08-10'),
    # Газпромнефть сняла лимиты в 13 регионах (4 Aug 2026)
    ('Республика Татарстан', None, 'Газпромнефть', 'все', 'отмена', 'лимиты сняты с 4 авг 2026', '30л бензин, 60л дизель',
     'https://www.instagram.com/p/DbnWu4Asjuj/', '2026-08-10'),
]

# Delete conflicting rows (same region+network+client_type+limit_type) before inserting
for r in restrictions:
    region, city, network, client_type, limit_type = r[0], r[1], r[2], r[3], r[4]
    db.execute("DELETE FROM restrictions WHERE region=? AND COALESCE(network,'')=COALESCE(?, '') AND COALESCE(client_type,'')=COALESCE(?, '') AND COALESCE(limit_type,'')=COALESCE(?, '')",
               (region, network, client_type, limit_type))

# Insert new restrictions
inserted = 0
for r in restrictions:
    db.execute('''INSERT INTO restrictions 
                  (region, city, network, client_type, limit_type, limit_value, previous_value, source_url, source_date, is_current)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)''', r)
    inserted += 1

db.commit()
print(f"Inserted {inserted} new restrictions")

# Final stats
print(f"\nFinal DB stats:")
print(f"Total restrictions: {db.execute('SELECT COUNT(*) FROM restrictions').fetchone()[0]}")
print(f"Active restrictions: {db.execute('SELECT COUNT(*) FROM restrictions WHERE is_current=1').fetchone()[0]}")
print(f"Prices: {db.execute('SELECT COUNT(*) FROM prices WHERE price IS NOT NULL').fetchone()[0]}")
print(f"History: {db.execute('SELECT COUNT(*) FROM prices_history').fetchone()[0]}")
db.close()
