#!/usr/bin/env python3
"""Insert fresh diesel restrictions - 2026-09-02"""
import sqlite3

db = sqlite3.connect('/root/diesel_limits/restrictions.db')
today = '2026-09-02'

restrictions = [
    ('Москва', None, 'Газпромнефть', 'все', 'объем', 'до 40 л бензина и дизеля в бак', None,
     'https://lenta.ru/articles/2026/08/19/', today),
    ('Москва', None, 'Татнефть', 'все', 'объем', 'до 50 л бензина, до 60 л дизеля', None,
     'https://www.rbc.ru/economics/19/08/2026/', today),
    ('Калужская область', None, None, 'все', 'чет-нечет', 'чет/нечет по номерам; дизель без ограничений; до 30 л бензина', None,
     'https://lenta.ru/articles/2026/08/19/', today),
    ('Липецкая область', None, 'Газпром, Лукойл, Teboil, Роснефть', 'все', 'чет-нечет', 'чет/нечет с 13 августа; дизель без ограничений; 30 л бензина на авто', None,
     'https://lenta.ru/articles/2026/08/19/', today),
    ('Оренбургская область', None, None, 'все', 'объем', 'дизель: до 60 л в городе, до 200 л на трассе; бензин 15-30 л; запрет в канистры', None,
     'https://www.sravni.ru/novost/2026/8/25/', today),
    ('Волгоградская область', None, 'Лукойл', 'все', 'объем', 'дизель: 60 л в городе, 200 л на трассе; бензин 40 л', '40 л бензина, без дизеля',
     'https://www.sravni.ru/novost/2026/8/25/', today),
    ('Астраханская область', None, None, 'все', 'объем', 'с 25 августа: АИ-92 и АИ-95 до 30 л; дизель по общим правилам', '40 л на авто',
     'https://www.sravni.ru/novost/2026/8/25/', today),
    ('Республика Алтай', None, None, 'все', 'объем', 'дизель до 100 л; бензин до 50 л; единые лимиты для всех районов', '30 л бензин, 50 л дизель',
     'https://lenta.ru/articles/2026/08/19/', today),
    ('Воронежская область', None, None, 'все', 'объем', 'дизель: 60-200 л на машину; бензин 30-40 л', None,
     'https://lenta.ru/articles/2026/08/19/', today),
    ('Республика Дагестан', None, None, 'физлица', 'объем', '20 л бензина, 50 л дизеля; только в бак', None,
     'https://lenta.ru/articles/2026/07/07/', today),
    ('Республика Карелия', None, None, 'все', 'объем', '20-60 л в одни руки; запрет в канистры', None,
     'https://lenta.ru/articles/2026/07/07/', today),
    ('Краснодарский край', None, None, 'все', 'объем', '20-30 л бензина, 30-60 л дизеля', None,
     'https://lenta.ru/articles/2026/07/07/', today),
    ('Приморский край', None, None, 'юридические', 'объем', 'дизель для большегрузов: до 100 л в городе, до 200 л на трассе', None,
     'https://lenta.ru/articles/2026/07/07/', today),
    ('Псковская область', None, 'Татнефть', 'все', 'объем', 'до 40 л дизеля; 20 л АИ-95', None,
     'https://lenta.ru/articles/2026/07/07/', today),
    ('Кемеровская область', None, None, 'все', 'объем', '40 л бензина, 80 л дизеля; на трассе до 200 л дизеля', None,
     'https://lenta.ru/twz/', today),
    ('Омская область', None, None, 'все', 'объем', '40 л бензина, 80 л дизеля; на трассе 200 л дизеля', None,
     'https://www.rbc.ru/economics/22/06/2026/', today),
    ('Ростовская область', None, None, 'все', 'объем', 'дизель: 60 л легковые, 200-300 л грузовые', None,
     'https://www.rbc.ru/economics/10/07/2026/', today),
    ('Калининградская область', None, None, 'физлица', 'объем', '30 л бензина, 60 л дизеля на авто', None,
     'https://www.aa.com.tr/ru/', today),
    ('Республика Татарстан', None, 'Газпромнефть', 'физлица', 'объем', '30 л бензина, 60 л дизеля', None,
     'https://www.aa.com.tr/ru/', today),
    ('Мурманская область', None, 'Лукойл', 'физлица', 'объем', '30 л бензина, 60 л дизеля', None,
     'https://www.aa.com.tr/ru/', today),
    ('Республика Саха (Якутия)', None, None, 'все', 'объем', '30 л бензина, 200 л дизеля; запрет в переносную тару', None,
     'https://www.aa.com.tr/ru/', today),
    ('Иркутская область', None, 'КрайсНефть', 'физлица', 'объем', 'до 30 л бензина на авто; до 20 л в канистры', None,
     'https://www.sravni.ru/novost/2026/8/25/', today),
    ('Кировская область', None, None, 'все', 'объем', '30 л бензина; до 100 л дизеля', None,
     'https://lenta.ru/articles/2026/07/07/', today),
    ('Тамбовская область', None, None, 'все', 'объем', '30 л бензина; дизель без ограничений; чет/нечет на Роснефть и Лукойл', None,
     'https://www.sravni.ru/novost/2026/8/25/', today),
    ('Санкт-Петербург', None, 'Лукойл', 'все', 'снятие', 'ограничения сняты с конца июля', None,
     'https://lenta.ru/articles/2026/08/19/', today),
    ('Республика Башкортостан', None, 'Татнефть', 'все', 'объем', 'повышенные лимиты: 50 л АИ-92/95, 400 л дизеля; АИ-98 без ограничений', None,
     'https://www.sravni.ru/novost/2026/8/25/', today),
    ('Ульяновская область', None, None, 'все', 'объем', 'до 100 л дизеля на некоторых АЗС', None,
     'https://lenta.ru/articles/2026/07/07/', today),
    ('Курганская область', None, None, 'все', 'объем', '40 л бензина, 80 л дизеля в городе; 200 л дизеля на трассе; только в бак', None,
     'https://lenta.ru/articles/2026/08/19/', today),
    ('Самарская область', None, None, 'все', 'объем', '40 л бензина и 100 л дизеля легковые, 300 л дизеля грузовые; только в бак', None,
     'https://news.mail.ru/economics/71391449/', today),
    ('Пензенская область', None, None, 'физлица', 'объем', '100 л бензина и 200 л дизеля; в канистру 20 л', None,
     'https://lenta.ru/articles/2026/08/19/', today),
    ('Республика Калмыкия', None, None, 'все', 'объем', 'дизель по общим правилам региона', None,
     'https://www.sravni.ru/novost/2026/8/25/', today),
]

count = 0
for r in restrictions:
    region, city, network, client_type, limit_type, limit_value, previous_value, source_url, source_date = r
    # Try to find existing row by unique key
    if network:
        existing = db.execute('SELECT id FROM restrictions WHERE region=? AND network=? AND client_type=? AND limit_type=?',
                              (region, network, client_type, limit_type)).fetchone()
    else:
        existing = db.execute('SELECT id FROM restrictions WHERE region=? AND (network IS NULL OR network="") AND client_type=? AND limit_type=?',
                              (region, client_type, limit_type)).fetchone()
    
    if existing:
        # Update existing row
        db.execute('''UPDATE restrictions SET limit_value=?, previous_value=COALESCE(?,limit_value),
                      source_url=?, source_date=?, is_current=1, updated_at=datetime('now')
                      WHERE id=?''', (limit_value, previous_value, source_url, source_date, existing[0]))
    else:
        db.execute('''INSERT INTO restrictions(region, city, network, client_type, limit_type, limit_value, previous_value, source_url, source_date, is_current, created_at, updated_at)
                      VALUES(?,?,?,?,?,?,?,?,?,?,datetime('now'),datetime('now'))''',
                   (region, city, network, client_type, limit_type, limit_value, previous_value, source_url, source_date, 1))
    count += 1

db.commit()
print(f'Inserted {count} fresh restrictions')

active = db.execute('SELECT COUNT(*) FROM restrictions WHERE is_current=1').fetchone()[0]
total = db.execute('SELECT COUNT(*) FROM restrictions').fetchone()[0]
changes = db.execute('SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL').fetchone()[0]
print(f'Active: {active}, Total: {total}, With changes: {changes}')
db.close()
