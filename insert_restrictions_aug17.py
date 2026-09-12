#!/usr/bin/env python3
"""Insert fresh restrictions on diesel for Aug 2026"""
import sqlite3

db = sqlite3.connect("/root/diesel_limits/restrictions.db")
cur = db.cursor()

# Fresh diesel restrictions from search results (August 2026)
# Schema: region, city, network, client_type, limit_type, limit_value, previous_value, source_url, source_date
restrictions = [
    ("Оренбургская область", None, None, "все", "объем", "60 л (город) / 200 л (трасса)", None,
     "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-14"),

    ("Ивановская область", None, None, "физлица", "объем", "60-200 л", None,
     "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-14"),

    ("Калининградская область", None, "Лукойл, Сургутнефтегаз", "все", "отмена", "без ограничений", "60-100 л",
     "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-14"),

    ("Красноярский край", None, None, "все", "смягчение", "отмена на некоторых АЗС", "30 л бензина, дизель ограничен",
     "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-13"),

    ("Крым", None, None, "физлица", "объем", "40 л", None,
     "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-14"),

    ("Севастополь", None, None, "физлица", "объем", "40 л", None,
     "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-14"),

    ("Курганская область", None, None, "все", "объем", "80 л (город) / 200 л (трасса)", None,
     "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-14"),

    ("Тюменская область", None, "Газпромнефть", "все", "объем", "80 л (город) / 200 л (трасса)", None,
     "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-14"),

    ("Якутия", None, None, "все", "объем", "50-200 л", None,
     "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-14"),

    ("Чувашия", None, "Татнефть", "все", "отмена (дизель)", "без ограничений", None,
     "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-14"),

    ("Дагестан", None, None, "физлица", "объем", "50 л", None,
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-06-25"),

    ("Кемеровская область", None, "Газпромнефть, Лукойл", "все", "объем", "80 л (город) / 200 л (трасса)", None,
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-08-01"),

    ("Томская область", None, None, "все", "объем", "80 л", None,
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-08-01"),

    ("Владимирская область", None, None, "все", "время", "7:00-10:00 запрет", None,
     "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-14"),

    ("Тверская область", None, None, "все", "время", "5:30-7:30 запрет", None,
     "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-14"),

    ("Воронежская область", None, "Лукойл", "все", "объем", "60 л (город) / 200 л (трасса)", None,
     "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-28"),

    ("Кировская область", None, "Движение", "все", "объем", "100 л", None,
     "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-07-15"),

    ("Республика Алтай", None, None, "все", "объем", "50 л (ряд районов) / 100 л (остальные)", None,
     "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-07-09"),

    ("Новосибирская область", None, None, "все", "объем", "60 л", None,
     "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-28"),

    ("Ростовская область", None, None, "все", "объем", "60 л (легковые) / 200 л (грузовики)", None,
     "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-28"),

    ("Самарская область", None, None, "все", "объем", "100 л (легковые) / 300 л (грузовики)", None,
     "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-28"),

    ("Ульяновская область", None, None, "все", "объем", "100 л (легковые) / 300 л (грузовики)", None,
     "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-28"),

    ("Пензенская область", None, None, "физлица", "объем", "200 л", None,
     "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-28"),

    ("Мордовия", None, None, "все", "объем", "60 л (легковые) / 300 л (грузовики)", None,
     "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-28"),

    ("Республика Карелия", None, None, "все", "объем", "60 л (обычные) / 250 л (большегрузы)", None,
     "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-28"),

    ("Республика Татарстан", None, "Татнефть", "все", "объем", "60 л (легковые) / 300 л (грузовики)", None,
     "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-28"),

    ("Вологодская область", None, None, "все", "объем", "60 л (город) / 200 л (трасса)", None,
     "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-07-01"),

    ("Мурманская область", None, "Лукойл", "все", "объем", "60 л", None,
     "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-07-01"),
]

for r in restrictions:
    region, city, network, client_type, limit_type, value, prev, source_url, date = r
    cur.execute("""
        INSERT OR REPLACE INTO restrictions
        (region, city, network, client_type, limit_type, limit_value, previous_value,
         source_url, source_date, is_current, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, datetime('now'))
    """, (region, city, network, client_type, limit_type, value, prev, source_url, date))

db.commit()

# Stats
total = cur.execute("SELECT COUNT(*) FROM restrictions").fetchone()[0]
active = cur.execute("SELECT COUNT(*) FROM restrictions WHERE is_current=1").fetchone()[0]
with_prev = cur.execute("SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL").fetchone()[0]
db.close()

print(f"Inserted {len(restrictions)} fresh restrictions")
print(f"Total restrictions: {total}, active: {active}, with previous_value: {with_prev}")
