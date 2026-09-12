import sqlite3

db = sqlite3.connect('/root/diesel_limits/restrictions.db')

# Свежие ограничения по данным августа 2026
restrictions = [
    # Москва
    ('Москва', 'Москва', 'Газпромнефть (городские)', 'все', 'объем', '30л бензин / 60л дизель', None,
     'https://finance.mail.ru/article/gde-prodazha-benzina-ogranichena-i-kogda-situaciya-normalizuetsya-69215852/', '2026-08-17'),
    ('Москва', 'Москва', 'Газпромнефть (трассовые)', 'все', 'объем', '30л бензин / 200л дизель', None,
     'https://finance.mail.ru/article/gde-prodazha-benzina-ogranichena-i-kogda-situaciya-normalizuetsya-69215852/', '2026-08-17'),
    ('Москва', 'Москва', 'Лукойл', 'все', 'объем', '20-30л', None,
     'https://finance.mail.ru/article/gde-prodazha-benzina-ogranichena-i-kogda-situaciya-normalizuetsya-69215852/', '2026-08-17'),

    # Омская область
    ('Омская область', None, 'все АЗС (город)', 'все', 'объем', '40л бензин / 80л дизель', None,
     'https://finance.mail.ru/article/gde-prodazha-benzina-ogranichena-i-kogda-situaciya-normalizuetsya-69215852/', '2026-08-17'),
    ('Омская область', None, 'все АЗС (трасса)', 'все', 'объем', '40л бензин / 200л дизель', None,
     'https://finance.mail.ru/article/gde-prodazha-benzina-ogranichena-i-kogda-situaciya-normalizuetsya-69215852/', '2026-08-17'),

    # Вологодская область
    ('Вологодская область', None, 'все АЗС (город)', 'все', 'объем', '30л бензин / 60л дизель', None,
     'https://finance.mail.ru/article/gde-prodazha-benzina-ogranichena-i-kogda-situaciya-normalizuetsya-69215852/', '2026-08-17'),
    ('Вологодская область', None, 'все АЗС (трасса)', 'все', 'объем', '30л бензин / 200л дизель', None,
     'https://finance.mail.ru/article/gde-prodazha-benzina-ogranichena-i-kogda-situaciya-normalizuetsya-69215852/', '2026-08-17'),

    # Мурманская область
    ('Мурманская область', None, 'Лукойл', 'все', 'объем', '30л бензин / 60л дизель', None,
     'https://finance.mail.ru/article/gde-prodazha-benzina-ogranichena-i-kogda-situaciya-normalizuetsya-69215852/', '2026-08-17'),
    ('Мурманская область', None, 'Роснефть', 'все', 'объем', '99л бензин / дизель без ограничений', None,
     'https://finance.mail.ru/article/gde-prodazha-benzina-ogranichena-i-kogda-situaciya-normalizuetsya-69215852/', '2026-08-17'),
    ('Мурманская область', None, 'Газпромнефть', 'все', 'объем', '30л бензин / 30л дизель (60л по карте лояльности)', None,
     'https://finance.mail.ru/article/gde-prodazha-benzina-ogranichena-i-kogda-situaciya-normalizuetsya-69215852/', '2026-08-17'),

    # Самарская область
    ('Самарская область', None, 'все АЗС', 'физлица', 'объем', '40л бензин / 100л дизель', None,
     'https://finance.mail.ru/article/gde-prodazha-benzina-ogranichena-i-kogda-situaciya-normalizuetsya-69215852/', '2026-08-17'),

    # Пензенская область
    ('Пензенская область', None, 'все АЗС', 'физлица', 'объем', '100л бензин / 200л дизель', None,
     'https://finance.mail.ru/article/gde-prodazha-benzina-ogranichena-i-kogda-situaciya-normalizuetsya-69215852/', '2026-08-17'),

    # Белгородская область
    ('Белгородская область', None, 'Лукойл', 'физлица', 'объем', '30л бензин / 60л дизель', None,
     'https://finance.mail.ru/article/gde-prodazha-benzina-ogranichena-i-kogda-situaciya-normalizuetsya-69215852/', '2026-08-17'),

    # Ульяновская область
    ('Ульяновская область', None, 'все АЗС', 'все', 'объем', '40л бензин / 100л дизель (легковые) / 300л дизель (грузовые)', None,
     'https://finance.mail.ru/article/gde-prodazha-benzina-ogranichena-i-kogda-situaciya-normalizuetsya-69215852/', '2026-08-17'),

    # Якутия
    ('Республика Саха (Якутия)', None, 'Саханефтегазсбыт', 'все', 'объем', '30л бензин / 200л дизель', None,
     'https://finance.mail.ru/article/gde-prodazha-benzina-ogranichena-i-kogda-situaciya-normalizuetsya-69215852/', '2026-08-17'),

    # Дагестан
    ('Республика Дагестан', None, 'все АЗС', 'физлица', 'объем', '20л бензин / 50л дизель', None,
     'https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm', '2026-07-04'),

    # Владимирская область
    ('Владимирская область', None, 'все АЗС', 'физлица', 'объем', '20-30л бензин / 40л дизель', None,
     'https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm', '2026-07-04'),

    # Ивановская область
    ('Ивановская область', None, 'все АЗС', 'физлица', 'объем', '30л бензин / 60л дизель', None,
     'https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm', '2026-07-04'),

    # Кемеровская область
    ('Кемеровская область', None, 'все АЗС (город)', 'физлица', 'объем', '40л бензин / 80л дизель', None,
     'https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm', '2026-07-04'),
    ('Кемеровская область', None, 'все АЗС (трасса)', 'физлица', 'объем', 'дизель до 200л', None,
     'https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm', '2026-07-04'),

    # Ямало-Ненецкий АО
    ('Ямало-Ненецкий автономный округ', None, 'отдельные АЗС', 'все', 'объем', '40-70л (зависит от АЗС)', None,
     'https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm', '2026-07-04'),

    # Кировская область
    ('Кировская область', None, 'Движение', 'все', 'объем', '30л бензин / 100л дизель', None,
     'https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/', '2026-07-08'),

    # Республика Татарстан
    ('Республика Татарстан', None, 'Газпром', 'все', 'объем', '30л бензин / 60л дизель', None,
     'https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/', '2026-07-08'),

    # Воронежская область
    ('Воронежская область', None, 'все АЗС', 'все', 'объем', '30л бензин / 60л дизель', None,
     'https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/', '2026-07-08'),

    # Красноярский край
    ('Красноярский край', None, 'Газпромнефть', 'все', 'объем', '40л бензин', None,
     'https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/', '2026-07-08'),

    # Республика Алтай
    ('Республика Алтай', 'Горно-Алтайск, Майминский, Чемальский, Чойский, Турочакский районы', 'все АЗС', 'все', 'объем', '30л бензин / 50л дизель в сутки', None,
     'https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/', '2026-07-08'),
    ('Республика Алтай', 'остальные районы', 'все АЗС', 'все', 'объем', '50л бензин / 100л дизель в сутки', None,
     'https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/', '2026-07-08'),

    # Томская область
    ('Томская область', 'Колпашевский, Асиновский, Зырянский, Тегульдетский районы', 'все АЗС', 'все', 'объем', '30-40л бензин / 80л дизель', None,
     'https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/', '2026-07-08'),
]

cnt = 0
for r in restrictions:
    region, city, network, client_type, limit_type, limit_value, prev, url, date = r
    try:
        db.execute('''
            INSERT OR REPLACE INTO restrictions(region,city,network,client_type,limit_type,limit_value,previous_value,source_url,source_date,is_current)
            VALUES(?,?,?,?,?,?,?,?,?,1)
        ''', (region, city, network, client_type, limit_type, limit_value, prev, url, date))
        cnt += 1
    except Exception as e:
        print(f'Error inserting {region}: {e}')

db.commit()
print(f'Inserted {cnt} restrictions')
db.close()
