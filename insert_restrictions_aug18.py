#!/usr/bin/env python3
"""Вставка ограничений на 18.08.2026 из sravni.ru, lenta.ru, rbc.ru"""
import sqlite3
from datetime import datetime

db = sqlite3.connect('/root/diesel_limits/restrictions.db')

restrictions = [
    # Из sravni.ru - самые свежие данные (август 2026)
    {
        "region": "Оренбургская область",
        "restriction_type": "объем",
        "target": "физлица",
        "value": "60 л в населенных пунктах, 200 л на трассах",
        "source_url": "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/",
        "effective_from": "2026-08-14",
        "is_current": 1
    },
    {
        "region": "Владимирская область",
        "restriction_type": "время",
        "target": "физлица",
        "value": "с 7:00 до 10:00 только экстренные службы и спецтехника",
        "source_url": "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/",
        "effective_from": "2026-08-01",
        "is_current": 1
    },
    {
        "region": "Ивановская область",
        "restriction_type": "объем",
        "target": "физлица",
        "value": "30 л бензина, 60-200 л дизеля",
        "source_url": "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/",
        "effective_from": "2026-07-02",
        "is_current": 1
    },
    {
        "region": "Калининградская область",
        "restriction_type": "объем",
        "target": "физлица",
        "value": "30 л бензина, 60-100 л дизеля (Лукойл и Сургутнефтегаз отменили)",
        "source_url": "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/",
        "effective_from": "2026-07-28",
        "is_current": 1,
        "previous_value": "без ограничений"
    },
    {
        "region": "Калужская область",
        "restriction_type": "четные/нечетные дни",
        "target": "физлица",
        "value": "четные номера по четным дням, нечетные по нечетным (не на трассах)",
        "source_url": "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/",
        "effective_from": "2026-07-01",
        "is_current": 1,
        "notes": "Дизель не ограничен"
    },
    {
        "region": "Краснодарский край",
        "restriction_type": "объем",
        "target": "физлица",
        "value": "20-30 л бензина, только в бак",
        "source_url": "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/",
        "effective_from": "2026-07-01",
        "is_current": 1
    },
    {
        "region": "Крым и Севастополь",
        "restriction_type": "объем",
        "target": "физлица",
        "value": "20 л бензина, 40 л дизеля, только в бак (бензин по QR-кодам)",
        "source_url": "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/",
        "effective_from": "2026-06-15",
        "is_current": 1
    },
    {
        "region": "Курганская область",
        "restriction_type": "объем",
        "target": "физлица",
        "value": "АЗС на трассах: 40 л бензина, 200 л дизеля; в населенных пунктах: 40 л бензина, 80 л дизеля",
        "source_url": "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/",
        "effective_from": "2026-07-01",
        "is_current": 1
    },
    {
        "region": "Нижегородская область",
        "restriction_type": "объем",
        "target": "физлица",
        "value": "30-60 л бензина, четные/нечетные дни",
        "source_url": "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/",
        "effective_from": "2026-07-01",
        "is_current": 1
    },
    {
        "region": "Тверская область",
        "restriction_type": "время",
        "target": "физлица",
        "value": "с 5:30 до 7:30 только экстренные службы и спецтехника",
        "source_url": "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/",
        "effective_from": "2026-07-01",
        "is_current": 1
    },
    {
        "region": "Тюменская область",
        "restriction_type": "объем",
        "target": "физлица",
        "value": "Газпромнефть: трассы 40 л бензина 200 л дизеля, населенные пункты 40 л бензина 80 л дизеля",
        "source_url": "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/",
        "effective_from": "2026-07-01",
        "is_current": 1
    },
    {
        "region": "Челябинская область",
        "restriction_type": "объем",
        "target": "физлица",
        "value": "20-30 л бензина",
        "source_url": "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/",
        "effective_from": "2026-07-01",
        "is_current": 1
    },
    {
        "region": "Якутия",
        "restriction_type": "объем",
        "target": "физлица",
        "value": "20-30 л бензина, 50-200 л дизеля (преимущественно по топливным картам)",
        "source_url": "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/",
        "effective_from": "2026-06-20",
        "is_current": 1
    },
    # Из lenta.ru
    {
        "region": "Дагестан",
        "restriction_type": "объем",
        "target": "физлица",
        "value": "20 л бензина, 50 л дизеля, только в бак, приоритет спецтранспорту",
        "source_url": "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm",
        "effective_from": "2026-06-25",
        "is_current": 1
    },
    {
        "region": "Республика Алтай",
        "restriction_type": "объем",
        "target": "физлица",
        "value": "Горно-Алтайск, Майминский, Чемальский, Чойский, Турочакский: 30 л бензина, 50 л дизеля; остальные районы: 50 л бензина, 100 л дизеля; до 1 сентября",
        "source_url": "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm",
        "effective_from": "2026-07-09",
        "effective_to": "2026-09-01",
        "is_current": 1
    },
    {
        "region": "Кировская область",
        "restriction_type": "объем",
        "target": "физлица",
        "value": "Лукойл: 30 л бензина; Движение: 20 л бензина; четные/нечетные дни",
        "source_url": "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm",
        "effective_from": "2026-07-01",
        "is_current": 1
    },
    {
        "region": "Кемеровская область",
        "restriction_type": "объем",
        "target": "физлица",
        "value": "Газпромнефть, Лукойл: 40 л бензина (10 л в канистру), 80 л дизеля; трассы: до 200 л дизеля",
        "source_url": "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm",
        "effective_from": "2026-07-01",
        "is_current": 1
    },
    # Из rbc.ru
    {
        "region": "Магаданская область",
        "restriction_type": "объем",
        "target": "физлица",
        "value": "полный бак, до 100 л бензина в сутки на ТС; дизель: в Магадане до 500 л, в других районах до 250 л; до сентября",
        "source_url": "https://prim.rbc.ru/prim/13/07/2026/6a5456e09a7947c742a14001",
        "effective_from": "2026-07-13",
        "is_current": 1
    },
    {
        "region": "Забайкальский край",
        "restriction_type": "QR-коды",
        "target": "физлица",
        "value": "15 л бензина по QR-кодам в боте Топливо 75 (тестовый режим)",
        "source_url": "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/",
        "effective_from": "2026-07-30",
        "is_current": 1
    },
]

inserted = 0
for r in restrictions:
    try:
        db.execute('''INSERT INTO restrictions 
            (region, limit_type, client_type, limit_value, source_url, source_date, is_current, previous_value, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))''',
            (r.get('region'), r.get('restriction_type'), r.get('target'), 
             r.get('value'), r.get('source_url'), r.get('effective_from'),
             r.get('is_current', 1), r.get('previous_value')))
        inserted += 1
    except Exception as e:
        print(f"Error inserting {r.get('region')}: {e}")

db.commit()
print(f"Inserted {inserted} restrictions")
db.close()
