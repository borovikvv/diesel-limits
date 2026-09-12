import sqlite3

db = sqlite3.connect('/root/diesel_limits/restrictions.db')

fresh = [
    # Sentyabr 2026 - pogorshenie situacii
    ('Краснодарский край', None, None, 'все', 'объём',
     'дежурство волонтёров и казаков для регулирования очередей; бензин до 30л/дизель до 60л',
     None, 'https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/', '2026-09-10'),
    ('Калужская область', None, None, 'все', 'время',
     'система чёт/нечет не касается дизельного топлива (доступно в любой день); трассовые АЗС без ограничений',
     None, 'https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/', '2026-09-10'),
    ('Ленинградская область', None, None, 'физлица', 'объём',
     'повторение июльского сценария: на ряде АЗС отгрузки снижены, возможны перебои',
     None, 'https://kazan.aif.ru/society/gde-ocheredi-benzin-v-rossii-na-10-sentyabrya-ceny-ocheredi-prognozy', '2026-09-10'),
    ('Татарстан', None, 'Лукойл, Teboil', 'физлица', 'запрет',
     'на многих АЗС Лукойл и Teboil бензин отсутствует, в продаже только дизельное топливо',
     None, 'https://kazan.aif.ru/society/gde-ocheredi-benzin-v-rossii-na-10-sentyabrya-ceny-ocheredi-prognozy', '2026-09-10'),
    ('Республика Крым', None, None, 'все', 'объём',
     'средняя цена бензина 169 руб/л, на отдельных АЗС превышает 200 руб; ДТ 156.94 руб/л',
     None, 'https://kazan.aif.ru/society/gde-ocheredi-benzin-v-rossii-na-10-sentyabrya-ceny-ocheredi-prognozy', '2026-09-10'),
    ('Республика Тыва', None, None, 'все', 'объём',
     'цена АИ-92 120.28, АИ-95 135.04, ДТ 114.32 руб/л',
     None, 'https://benzup.ru/index-region', '2026-08-25'),
    ('Донецкая Народная Республика', None, None, 'все', 'объём',
     'цена АИ-92 127.75, АИ-95 144.40, ДТ 147.40 руб/л',
     None, 'https://benzup.ru/index-region', '2026-08-25'),
    ('Луганская Народная Республика', None, None, 'все', 'объём',
     'цена АИ-92 114.70, АИ-95 119.52, ДТ 122.63 руб/л',
     None, 'https://benzup.ru/index-region', '2026-08-25'),
    ('Магаданская область', None, None, 'все', 'объём',
     'ДТ 112.90 руб/л - один из самых дорогих регионов',
     None, 'https://benzup.ru/index-region', '2026-08-25'),
    ('Республика Саха (Якутия)', None, None, 'все', 'объём',
     'ДТ 112.26 руб/л',
     None, 'https://benzup.ru/index-region', '2026-08-25'),
    ('Забайкальский край', None, None, 'все', 'объём',
     'ДТ 100.29 руб/л',
     None, 'https://benzup.ru/index-region', '2026-08-25'),
    ('Камчатский край', None, None, 'все', 'объём',
     'ДТ 109.16 руб/л',
     None, 'https://benzup.ru/index-region', '2026-08-25'),
    ('Ханты-Мансийский автономный округ', None, None, 'все', 'объём',
     'ДТ 95.79 руб/л',
     None, 'https://benzup.ru/index-region', '2026-08-25'),
    ('Чукотский автономный округ', None, None, 'все', 'объём',
     'ДТ 84.22 руб/л',
     None, 'https://benzup.ru/index-region', '2026-08-25'),
]

inserted = 0
for row in fresh:
    region, city, network, client_type, limit_type, limit_value, prev, url, date = row
    db.execute('''INSERT INTO restrictions(region, city, network, client_type, limit_type,
               limit_value, previous_value, source_url, source_date, is_current,
               created_at, updated_at)
               VALUES(?,?,?,?,?,?,?, ?,?,1, datetime('now'), datetime('now'))''',
               (region, city, network, client_type, limit_type, limit_value, prev, url, date))
    inserted += 1

db.commit()
print(f"Inserted: {inserted}")

# Stats
active = db.execute("SELECT COUNT(*) FROM restrictions WHERE is_current=1").fetchone()[0]
total = db.execute("SELECT COUNT(*) FROM restrictions").fetchone()[0]
changes = db.execute("SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL").fetchone()[0]
print(f"Active: {active}, Total: {total}, With changes: {changes}")

db.close()
