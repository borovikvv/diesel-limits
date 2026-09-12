#!/usr/bin/env python3
"""Insert restrictions Aug 11, 2026 — fresh data from searches."""
import sqlite3
from datetime import datetime

db = sqlite3.connect('/root/diesel_limits/restrictions.db')
today = '2026-08-11'

# (region, city, network, client_type, limit_type, limit_value, previous_value, source_url, source_date)
restrictions_data = [
    # Дагестан (обновлено)
    ('Республика Дагестан', None, 'все сети', 'физлица', 'объем', '20 л бензин, 50 л дизель', '10 л бензин, 20 л дизель', 
     'https://kavkaz.rbc.ru/kavkaz/freenews/6a3ce7d19a79476809853bb1', '2026-06-25'),
    
    # Воронежская область
    ('Воронежская область', None, 'все сети', 'все', 'объем', '30 л бензин, 60 л дизель', None,
     'https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182', '2026-07-01'),
    
    # Калининградская область
    ('Калининградская область', None, 'все сети', 'все', 'объем', '30 л бензин, 60 л дизель', None,
     'https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182', '2026-07-01'),
    
    # Татарстан (Газпромнефть)
    ('Республика Татарстан', None, 'Газпромнефть', 'все', 'объем', '30 л бензин, 60 л дизель', None,
     'https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182', '2026-07-01'),
    
    # Мурманская область (Lukoil)
    ('Мурманская область', None, 'Лукойл', 'все', 'объем', '30 л бензин, 60 л дизель', None,
     'https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182', '2026-07-01'),
    
    # Омская область
    ('Омская область', None, 'все сети', 'все', 'объем', '40 л бензин, 80 л дизель (трассовые 200 л)', None,
     'https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182', '2026-07-01'),
    
    # Кемеровская область
    ('Кемеровская область', None, 'все сети', 'все', 'объем', '40 л бензин, 80 л дизель (трассовые 200 л)', None,
     'https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182', '2026-07-01'),
    
    # Якутия
    ('Республика Саха (Якутия)', None, 'все сети', 'все', 'объем', '30 л бензин, 200 л дизель + запрет в переносные емкости', None,
     'https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182', '2026-07-01'),
    
    # Магаданская область (новое)
    ('Магаданская область', 'Магадан', 'все сети', 'все', 'объем', 'дизель до 500 л/сутки в Магадане, до 250 л/сутки в районах', None,
     'https://prim.rbc.ru/prim/13/07/2026/6a5456e09a7947c742a14001', '2026-07-13'),
    
    # Самарская область
    ('Самарская область', None, 'все сети', 'все', 'объем', '40 л бензин, 100 л дизель', None,
     'https://www.kommersant.ru/doc/8764043', '2026-06-24'),
    
    # Новосибирская область
    ('Новосибирская область', None, 'все сети', 'все', 'объем', '40 л бензин, 80 л дизель', None,
     'https://moika78.ru/news/2026-06-23/1320351-v-kakih-regionah-rossii-vveli-limity-na-prodazhu-benzina-a-chto-v-peterburge-i-lenoblasti/', '2026-06-23'),
    
    # Краснодарский край
    ('Краснодарский край', None, 'все сети', 'все', 'объем', '20-30 л бензин, 30-60 л дизель', None,
     'https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/', '2026-07-07'),
    
    # Приморский край (большегрузы)
    ('Приморский край', None, 'все сети', 'грузовики', 'объем', '100 л дизель в городе, 200 л на трассе', None,
     'https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/', '2026-07-07'),
    
    # Кировская область
    ('Кировская область', None, 'все сети', 'все', 'объем', '30-100 л бензин, до 100 л дизель', None,
     'https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm', '2026-07-03'),
    
    # Севастополь
    ('Севастополь', None, 'все сети', 'все', 'время', 'ограниченная продажа, открыты 8 АЗС, до конца июля', None,
     'https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm', '2026-07-03'),
    
    # Москва
    ('Москва', None, 'все сети', 'физлица', 'объем', '20-30 л бензин, до 60 л дизель (трассовые до 200 л)', None,
     'https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm', '2026-07-03'),
    
    # Татнефть (федеральная сеть)
    ('Российская Федерация', None, 'Татнефть', 'все', 'объем', '20 л бензин, 40 л дизель легковые, 300 л грузовики', None,
     'https://amp.rbc.ru/rbcnews/society/16/06/2026/6a31181c9a794709b41eb0e5', '2026-06-16'),
    
    # Лукойл (федеральная сеть)
    ('Российская Федерация', None, 'Лукойл', 'физлица', 'объем', '30 л бензин, 60 л дизель', None,
     'https://www.fontanka.ru/2026/06/23/76495132/', '2026-06-23'),
    
    # Газпромнефть (федеральная сеть)
    ('Российская Федерация', None, 'Газпромнефть', 'все', 'объем', '30 л бензин, 30 л дизель', None,
     'https://m.vk.com/wall-65457623_44077', '2026-07-07'),
    
    # Роснефть (федеральная сеть)
    ('Российская Федерация', None, 'Роснефть', 'все', 'объем', '99 л бензин, дизель без ограничений', None,
     'https://m.vk.com/wall-65457623_44077', '2026-07-07'),
]

inserted = 0
for r in restrictions_data:
    region, city, network, client_type, limit_type, limit_value, previous_value, source_url, source_date = r
    db.execute('''INSERT OR REPLACE INTO restrictions 
                  (region, city, network, client_type, limit_type, limit_value, previous_value, source_url, source_date, is_current, created_at, updated_at)
                  VALUES (?,?,?,?,?,?,?,?,?,1,datetime("now"),datetime("now"))''',
               (region, city, network, client_type, limit_type, limit_value, previous_value, source_url, source_date))
    inserted += 1

db.commit()
print(f'Insertions: {inserted}')

# Check totals
active = db.execute('SELECT COUNT(*) FROM restrictions WHERE is_current=1').fetchone()[0]
total = db.execute('SELECT COUNT(*) FROM restrictions').fetchone()[0]
with_prev = db.execute('SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL').fetchone()[0]
print(f'Active: {active}, Total: {total}, With previous_value: {with_prev}')
db.close()
