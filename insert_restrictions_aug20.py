import sqlite3

db = sqlite3.connect('/root/diesel_limits/restrictions.db')

# Обновления на 20 августа 2026
# Вторая волна ограничений + смягчения в отдельных регионах

updates = [
    # === ВТОРАЯ ВОЛНА ОГРАНИЧЕНИЙ (август 2026) ===
    # По данным sravni.ru от 19.08.2026 - новая волна ограничений
    ('Россия (федеральный уровень)', None, 'все АЗС', 'физлица', 'объем', '30л на авто / 20л в канистры (дизель)', None,
     'https://www.sravni.ru/novost/2026/8/19/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-19'),

    # По данным oilcapital.ru от 12.08.2026
    ('Россия (федеральный уровень)', None, 'все АЗС', 'все', 'объем', 'бензин 15-30л / дизель до 60л (город)', None,
     'https://oilcapital.ru/news/2026-08-12/limity-na-otpusk-topliva-na-rossiyskih-azs-vvodyat-po-vtoromu-krugu-5657890', '2026-08-12'),

    # konkurent.ru - ограничения возвращаются, Приморский край
    ('Приморский край', None, 'Лукойл, Газпром', 'все', 'объем', '40л на автомобиль', None,
     'https://konkurent.ru/article/90474', '2026-08-13'),

    # === СМЯГЧЕНИЯ (июль-август 2026) ===
    # Крым - свободная продажа на 99 АЗС
    ('Республика Крым', None, '99 АЗС (разные сети)', 'все', 'объем', 'свободная продажа (бензин + дизель)', None,
     'https://finance.mail.ru/article/nu-vot-i-vse-v-kakih-regionah-nachali-snimat-ogranicheniya-na-prodazhu-benzina-i-dizelya-69219723/', '2026-07-18'),

    # Адыгея - лимит увеличен до 40л
    ('Республика Адыгея', None, 'все АЗС', 'все', 'объем', '40л (увеличен с 20-30л)', '20-30л',
     'https://finance.mail.ru/article/nu-vot-i-vse-v-kakih-regionah-nachali-snimat-ogranicheniya-na-prodazhu-benzina-i-dizelya-69219723/', '2026-07-21'),

    # Карелия - бензин до 40л, дизель без изменений
    ('Республика Карелия', None, 'все АЗС', 'физлица', 'объем', '40л бензин / 60л дизель / 250л дизель (грузовые)', '30л бензин',
     'https://finance.mail.ru/article/nu-vot-i-vse-v-kakih-regionah-nachali-snimat-ogranicheniya-na-prodazhu-benzina-i-dizelya-69219723/', '2026-07-18'),

    # Саратовская область - бензин до 40л
    ('Саратовская область', None, 'все АЗС', 'все', 'объем', '40л бензин в сутки', '30л',
     'https://finance.mail.ru/article/nu-vot-i-vse-v-kakih-regionah-nachali-snimat-ogranicheniya-na-prodazhu-benzina-i-dizelya-69219723/', '2026-07-27'),

    # Вологодская область - Лукойл увеличил до 40л
    ('Вологодская область', None, 'Лукойл', 'все', 'объем', '40л (увеличен с 30л)', '30л',
     'https://finance.mail.ru/article/nu-vot-i-vse-v-kakih-regionah-nachali-snimat-ogranicheniya-na-prodazhu-benzina-i-dizelya-69219723/', '2026-07-18'),

    # Ленинградская область - снятие ограничений
    ('Ленинградская область', 'Санкт-Петербург', 'отдельные АЗС', 'все', 'объем', 'сняты (ранее 20-30л бензин)', '20-30л бензин',
     'https://finance.mail.ru/article/nu-vot-i-vse-v-kakih-regionah-nachali-snimat-ogranicheniya-na-prodazhu-benzina-i-dizelya-69219723/', '2026-07-14'),

    # Псковская область - смягчение для деревень
    ('Псковская область', None, 'все АЗС', 'все', 'объем', '40л дизель (смягчение для деревень)', None,
     'https://finance.mail.ru/article/nu-vot-i-vse-v-kakih-regionah-nachali-snimat-ogranicheniya-na-prodazhu-benzina-i-dizelya-69219723/', '2026-07-18'),

    # === ТОПЛИВНЫЕ КАРТЫ ===
    # Лукойл отменил лимит на дизель по картам с 15 июля 2026
    ('Россия (федеральный уровень)', None, 'Лукойл (топливные карты)', 'юридические', 'объем', 'лимит на дизель отменён (с 15.07.2026)', 'ранее были лимиты',
     'https://www.asmap-service.ru/news/c_15_iyulya_2026_goda_otmenyen_limit_na_dizelnoe_toplivo_po_virtualnym_i_plastikovym_kartam_lukoyl/', '2026-07-15'),

    # === ОБНОВЛЕНИЯ ПО РЕГИОНАМ (август 2026) ===
    # Москва / Московская область
    ('Москва', 'Москва', 'Газпромнефть (городские)', 'все', 'объем', '30л бензин / 60л дизель', None,
     'https://www.sravni.ru/novost/2026/8/19/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-19'),
    ('Москва', 'Москва', 'Газпромнефть (трассовые)', 'все', 'объем', '30л бензин / 200л дизель', None,
     'https://www.sravni.ru/novost/2026/8/19/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-19'),
    ('Москва', 'Москва', 'Лукойл', 'все', 'объем', '20-30л', None,
     'https://www.sravni.ru/novost/2026/8/19/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-19'),

    # Омская область
    ('Омская область', None, 'все АЗС (город)', 'все', 'объем', '40л бензин / 80л дизель', None,
     'https://www.sravni.ru/novost/2026/8/19/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-19'),
    ('Омская область', None, 'все АЗС (трасса)', 'все', 'объем', '40л бензин / 200л дизель', None,
     'https://www.sravni.ru/novost/2026/8/19/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/', '2026-08-19'),

    # Краснодарский край
    ('Краснодарский край', None, 'разные АЗС', 'все', 'объем', '20-30л бензин / 30-60л дизель', None,
     'https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/', '2026-08-19'),

    # Приморский край - для большегрузов
    ('Приморский край', None, 'АЗС в черте города', 'грузовые', 'объем', '100л дизель', None,
     'https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/', '2026-08-19'),
    ('Приморский край', None, 'трассовые АЗС', 'грузовые', 'объем', '200л дизель', None,
     'https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/', '2026-08-19'),

    # Псковская область / Удмуртия - дизель
    ('Псковская область', None, 'все АЗС', 'все', 'объем', '40л дизель', None,
     'https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/', '2026-08-19'),
    ('Удмуртская Республика', None, 'все АЗС', 'все', 'объем', '40л дизель', None,
     'https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/', '2026-08-19'),

    # Кировская / Ульяновская области
    ('Кировская область', None, 'отдельные АЗС', 'все', 'объем', 'до 100л дизель', None,
     'https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/', '2026-08-19'),
    ('Ульяновская область', None, 'отдельные АЗС', 'все', 'объем', 'до 100л дизель', None,
     'https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/', '2026-08-19'),

    # Мурманская область
    ('Мурманская область', None, 'Лукойл', 'все', 'объем', '30л бензин / 60л дизель', None,
     'https://finance.mail.ru/article/gde-prodazha-benzina-ogranichena-i-kogda-situaciya-normalizuetsya-69215852/', '2026-08-19'),
    ('Мурманская область', None, 'Роснефть', 'все', 'объем', '99л бензин / дизель без ограничений', None,
     'https://finance.mail.ru/article/gde-prodazha-benzina-ogranichena-i-kogda-situaciya-normalizuetsya-69215852/', '2026-08-19'),
    ('Мурманская область', None, 'Газпромнефть', 'все', 'объем', '30л бензин / 30л дизель (60л по карте)', None,
     'https://finance.mail.ru/article/gde-prodazha-benzina-ogranichena-i-kogda-situaciya-normalizuetsya-69215852/', '2026-08-19'),

    # Белгородская область
    ('Белгородская область', None, 'Лукойл', 'физлица', 'объем', '30л бензин / 60л дизель (200л дизель на трассе)', None,
     'https://alfabank.ru/alfa-investor/posts/t/9d87c0ea-9a70-f111-91c8-0050569e1fd0/', '2026-08-19'),

    # Новосибирская область
    ('Новосибирская область', None, 'все АЗС', 'все', 'объем', '40л бензин / 80л дизель', None,
     'https://moika78.ru/news/2026-06-23/1320351-v-kakih-regionah-rossii-vveli-limity-na-prodazhu-benzina-a-chto-v-peterburge-i-lenoblasti/', '2026-08-19'),

    # Кемеровская область
    ('Кемеровская область', None, 'все АЗС (город)', 'физлица', 'объем', '40л бензин / 80л дизель', None,
     'https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/', '2026-08-19'),
    ('Кемеровская область', None, 'все АЗС (трасса)', 'физлица', 'объем', 'дизель до 200л', None,
     'https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/', '2026-08-19'),

    # Республика Алтай - дифференцированные лимиты
    ('Республика Алтай', 'Горно-Алтайск и ряд районов', 'все АЗС', 'все', 'объем', '30л бензин / 50л дизель в сутки', None,
     'https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/', '2026-08-19'),
    ('Республика Алтай', 'остальные районы', 'все АЗС', 'все', 'объем', '50л бензин / 100л дизель в сутки', None,
     'https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/', '2026-08-19'),
]

cnt = 0
new_cnt = 0
changed_cnt = 0
for r in updates:
    region, city, network, client_type, limit_type, limit_value, prev, url, date = r
    try:
        # Check if exists
        existing = db.execute(
            'SELECT limit_value, previous_value FROM restrictions WHERE region=? AND network=? AND client_type=? AND limit_type=?',
            (region, network, client_type, limit_type)
        ).fetchone()
        if existing:
            if existing[0] != limit_value:
                # Value changed, update
                db.execute('''UPDATE restrictions SET limit_value=?, previous_value=?, source_url=?, source_date=?, is_current=1, updated_at=datetime("now")
                    WHERE region=? AND network=? AND client_type=? AND limit_type=?''',
                    (limit_value, existing[0] if prev is None else prev, url, date, region, network, client_type, limit_type))
                changed_cnt += 1
            cnt += 1
        else:
            db.execute('''INSERT OR REPLACE INTO restrictions(region,city,network,client_type,limit_type,limit_value,previous_value,source_url,source_date,is_current)
                VALUES(?,?,?,?,?,?,?,?,?,1)''', (region, city, network, client_type, limit_type, limit_value, prev, url, date))
            new_cnt += 1
            cnt += 1
    except Exception as e:
        print(f'Error: {region} / {network}: {e}')

db.commit()
print(f'Total processed: {cnt}, new: {new_cnt}, changed: {changed_cnt}')

# Count stats
active = db.execute('SELECT COUNT(*) FROM restrictions WHERE is_current=1').fetchone()[0]
with_prev = db.execute('SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL AND is_current=1').fetchone()[0]
print(f'Active restrictions: {active}, with previous_value: {with_prev}')
db.close()
