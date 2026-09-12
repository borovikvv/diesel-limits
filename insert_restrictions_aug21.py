#!/usr/bin/env python3
"""Insert fresh diesel restrictions from Aug 19-21 2026 sources."""
import sqlite3
from datetime import datetime

db = sqlite3.connect('/root/diesel_limits/restrictions.db')
today = '2026-08-21'

# (region, city, azs_network, client_type, limit_type, value, source_url, source_date, is_current)
restrictions = [
    # NEW: Krasnoyarsk kraй - cancel diesel limits on some AZS
    ("Красноярский край", "Красноярск", "Газпромнефть", "все", "объем", "некоторые АЗС отменили лимиты на ДТ", "https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/", "2026-08-19", 1),
    # Krasnodar kraй
    ("Краснодарский край", None, "сетевые АЗС", "физлица", "объем", "30 л бензин, 10 л в канистры; дизель без ограничений", "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-07-01", 1),
    # Orenburg - NEW system chet-nechet + diesel limits
    ("Оренбургская область", None, "все АЗС", "физлица+юрлица", "объем", "ДТ: до 60 л (город), до 200 л (трассы); бензин 15-30 л; система чет/нечет с 12.08", "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-12", 1),
    # Volgograd - repeated limits
    ("Волгоградская область", None, "Лукойл, Газпром", "физлица", "объем", "40 л бензин; Лукойл: 60 л ДТ (город), 200 л ДТ (трасса)", "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-01", 1),
    # Astrakhan - repeated
    ("Астраханская область", None, "Лукойл, Газпром", "физлица", "объем", "40 л бензин; Лукойл: 60 л ДТ", "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-13", 1),
    # Kaluga - NEW chet-nechet (diesel exempt)
    ("Калужская область", None, "сетевые АЗС", "физлица", "объем+время", "система чет/нечет с 15.08; 30 л бензин; дизель без ограничений; только в бак", "https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/", "2026-08-15", 1),
    # Lipetsk - NEW chet-nechet
    ("Липецкая область", None, "Газпром, Лукойл, Teboil, Роснефть", "физлица", "объем+время", "система чет/нечет с 13.08; 30 л бензин; дизель без ограничений; трассы М-4,Р-119,А-133 exempt", "https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/", "2026-08-13", 1),
    # Rep. Altai - softened
    ("Республика Алтай", "Горно-Алтайск", "сетевые АЗС", "физлица", "объем", "50 л бензин, 100 л дизель (увеличено с 30/50); в канистры 10 л по СТС; до 01.09.2026", "https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/", "2026-08-11", 1),
    # Dagestan
    ("Республика Дагестан", None, "все АЗС", "физлица", "объем", "20 л бензин, 50 л дизель; только в бак", "https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/", "2026-08-19", 1),
    # Nizhny Novgorod
    ("Нижегородская область", None, "сетевые АЗС", "физлица", "объем", "30-40 л бензин, можно в канистры", "https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/", "2026-08-19", 1),
    # Chelyabinsk
    ("Челябинская область", None, "сетевые АЗС", "физлица", "объем", "20-40 л бензин", "https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/", "2026-08-19", 1),
    # Murmansk
    ("Мурманская область", None, "Лукойл, Газпромнефть", "физлица", "объем+запрет", "30 л бензин; Лукойл: 60 л дизель; Газпромнефть: 30 л дизель; запрет на канистры", "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-07-01", 1),
    # Orel + Irkutsk
    ("Орловская область", None, "сетевые АЗС", "физлица", "объем", "30 л бензин (город), 50 л (трасса)", "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-07-01", 1),
    ("Иркутская область", None, "КрайсНефть", "физлица", "объем", "30 л бензин на авто, 20 л в канистры; с 13.08", "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-13", 1),
    # Zabaykalsky krai
    ("Забайкальский край", None, "сетевые АЗС", "физлица", "объем", "15-20 л бензин на машину", "https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/", "2026-08-19", 1),
    # Moscow AZS limits
    ("Москва", None, "Газпромнефть", "физлица", "объем", "до 60 л бензин; дизель до 40 л в бак", "https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/", "2026-08-19", 1),
    ("Москва", None, "Татнефть", "физлица", "объем", "до 50 л бензин, до 60 л дизель", "https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/", "2026-08-19", 1),
    # Yakutia
    ("Республика Саха (Якутия)", None, "сетевые АЗС", "физлица", "объем+запрет", "20-30 л бензин, 50-200 л дизель; запрет на канистры на некоторых АЗС; только по топливным картам или в бак", "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-14", 1),
    # Tambov - partial cancel
    ("Тамбовская область", None, "несетевые АЗС", "физлица", "отмена", "отменена система чет/нечет на несетевых АЗС с 14.08; разрешены канистры; на Роснефть/Лукойл чет/нечет сохраняется; 30 л бензин", "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-14", 1),
    # Samara
    ("Самарская область", None, "сетевые АЗС", "физлица", "объем", "40 л бензин", "https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/", "2026-08-19", 1),
    # Kurgan
    ("Курганская область", None, "сетевые АЗС", "физлица", "объем", "40 л бензин", "https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/", "2026-08-19", 1),
    # Adygea
    ("Республика Адыгея", None, "сетевые АЗС", "физлица", "объем", "40 л бензин", "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-14", 1),
    # Arkhangelsk
    ("Архангельская область", None, "сетевые АЗС", "физлица", "объем", "20-50 л бензин в зависимости от АЗС", "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-14", 1),
    # Voronezh
    ("Воронежская область", None, "сетевые АЗС", "физлица", "объем", "30 л бензин, 60 л дизель", "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-07-01", 1),
    # Kaliningrad
    ("Калининградская область", None, "Лукойл, Сургутнефтегаз", "физлица", "объем", "бензин сняли; ранее 30 л бензин, 60 л дизель", "https://www.sravni.ru/novost/2026/8/14/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-07-28", 1),
]

inserted = 0
for r in restrictions:
    region, city, azs, client, ltype, value, url, sdate, is_current = r
    db.execute('''INSERT OR REPLACE INTO restrictions
        (region, city, network, client_type, limit_type, limit_value,
         source_url, source_date, is_current, previous_value)
        VALUES (?,?,?,?,?,?,?,?,?,?)''',
        (region, city, azs, client, ltype, value, url, sdate, is_current, None))
    inserted += 1

db.commit()
db.close()
print(f"Inserted {inserted} restrictions")
