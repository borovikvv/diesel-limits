import sqlite3

db = sqlite3.connect('/root/diesel_limits/restrictions.db')

# Current restrictions (Aug/Sep 2026) - extracted from web searches
restrictions = [
    # (region, city, network, client_type, limit_type, limit_value, source_url, source_date)
    
    # Дагестан - с 25 июня
    ('Республика Дагестан', None, None, 'физлица', 'объем', '20л бензин, 50л дизель', 
     'https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm', '2026-06-25'),
    
    # Воронежская область - с 23 июня
    ('Воронежская область', None, None, 'все', 'объем', '30л бензин, 60л дизель',
     'https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/', '2026-06-23'),
    
    # Владимирская область - с 18 июня
    ('Владимирская область', None, None, 'физлица', 'объем', '20-30л бензин, 40л дизель',
     'https://vladtv.ru/society/172950/', '2026-06-18'),
    
    # Ивановская область - с 2 июля
    ('Ивановская область', None, None, 'все', 'объем', '30л бензин, 60л дизель',
     'https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/', '2026-07-02'),
    
    # Кемеровская область
    ('Кемеровская область', None, 'Газпромнефть', 'физлица', 'объем', '40л бензин, 80л дизель',
     'https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm', '2026-07'),
    ('Кемеровская область', None, None, 'грузовики', 'объем', 'до 200л дизель (трассы)',
     'https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm', '2026-07'),
    
    # Москва
    ('Москва', None, 'Газпромнефть', 'все', 'объем', '20-30л бензин, 60л дизель',
     'https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm', '2026-07'),
    ('Москва', None, None, 'все', 'объем', 'до 200л дизель (трассы)',
     'https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm', '2026-07'),
    
    # Татарстан
    ('Республика Татарстан', None, 'Газпромнефть', 'все', 'объем', '30л бензин, 60л дизель',
     'https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/', '2026-07'),
    
    # Мурманская область
    ('Мурманская область', None, 'Лукойл', 'все', 'объем', '30л бензин, 60л дизель',
     'https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/', '2026-07'),
    
    # Краснодарский край
    ('Краснодарский край', None, None, 'все', 'объем', '20-30л бензин, 30-60л дизель',
     'https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/', '2026-07'),
    
    # Республика Алтай - увеличены лимиты
    ('Республика Алтай', 'Горно-Алтайск', None, 'все', 'объем', '50л бензин, 100л дизель',
     'https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/', '2026-08'),
    
    # Калининградская область
    ('Калининградская область', None, None, 'все', 'объем', '30л бензин, 60л дизель',
     'https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182', '2026-07'),
    
    # Якутия
    ('Республика Саха (Якутия)', None, None, 'все', 'объем', '30л бензин, 200л дизель',
     'https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182', '2026-07'),
    ('Республика Саха (Якутия)', None, None, 'все', 'запрет', 'запрет продажи в канистры',
     'https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182', '2026-07'),
    
    # Астраханская область - с 13 августа
    ('Астраханская область', None, None, 'все', 'объем', 'до 40л',
     'https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-13'),
    
    # Ростовская область
    ('Ростовская область', None, None, 'легковые', 'объем', 'до 60л дизель',
     'https://rostov.rbc.ru/rostov/freenews/6a8c471b9a79471ebfd2f55d', '2026-07'),
    
    # Кировская область
    ('Кировская область', None, 'Движение', 'все', 'объем', '30л бензин, 100л дизель',
     'https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/', '2026-07'),
    
    # Липецкая область - на дизель ограничений нет
    ('Липецкая область', None, None, 'все', 'объем', 'ограничений на дизель нет',
     'https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/', '2026-08'),
    
    # Приморский край - для большегрузов
    ('Приморский край', None, None, 'грузовики', 'объем', 'до 100л дизель (город), до 200л (трасса)',
     'https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/', '2026-07'),
]

inserted = 0
for region, city, network, client_type, limit_type, limit_value, source_url, source_date in restrictions:
    try:
        db.execute('''INSERT OR REPLACE INTO restrictions 
                     (region, city, network, client_type, limit_type, limit_value, 
                      source_url, source_date, is_current, updated_at)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, datetime("now"))''',
                  (region, city, network, client_type, limit_type, limit_value, source_url, source_date))
        inserted += 1
    except Exception as e:
        print(f"Error inserting {region}: {e}")

db.commit()
print(f'Inserted/updated {inserted} restrictions')

# Count active
active = db.execute('SELECT COUNT(*) FROM restrictions WHERE is_current=1').fetchone()[0]
print(f'Total active restrictions: {active}')

db.close()
