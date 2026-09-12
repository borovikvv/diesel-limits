#!/usr/bin/env python3
"""Insert fresh diesel restrictions from web sources (Aug 9, 2026)."""
import sqlite3

DB = sqlite3.connect('/root/diesel_limits/restrictions.db')

# Fresh restrictions from lenta.ru, sravni.ru, aa.com.tr (July-Aug 2026)
restrictions = [
    # (region, city, network, client_type, limit_type, limit_value, previous_value, source_url, source_date)
    ("Республика Дагестан", None, None, "физлица", "объем", "50 л дизель", "30 л", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-06-25"),
    ("Воронежская область", None, None, "все", "объем", "60 л дизель", None, "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-07-01"),
    ("Калининградская область", None, None, "все", "объем", "60 л дизель", None, "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-07-01"),
    ("Омская область", None, None, "все", "объем", "80 л дизель (город), 200 л (трасса для грузовиков)", "40 л", "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-07-01"),
    ("Кемеровская область", None, None, "все", "объем", "80 л дизель", "40 л", "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-07-01"),
    ("Республика Саха (Якутия)", None, None, "все", "объем", "200 л дизель", "30 л", "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-07-01"),
    ("Республика Татарстан", None, "Газпромнефть", "все", "объем", "60 л дизель", "30 л", "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-07-01"),
    ("Мурманская область", None, "Лукойл", "все", "объем", "60 л дизель", "30 л", "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-07-01"),
    ("Пензенская область", None, None, "все", "объем", "200 л дизель", None, "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-07-01"),
    ("Саратовская область", None, None, "все", "объем", "30 л дизель", None, "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-07-01"),
    ("Забайкальский край", None, None, "все", "объем", "15 л бензин, 100 л дизель", None, "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-07-01"),
    ("Кировская область", None, None, "все", "объем", "100 л дизель", None, "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-03"),
    ("Москва", None, None, "все", "объем", "60 л дизель (город), 200 л (трасса)", None, "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-03"),
    ("Севастополь", None, None, "все", "запрет", "ограниченная продажа до конца июля", None, "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-03"),
]

n = 0
for r in restrictions:
    region, city, network, client_type, limit_type, limit_value, prev, url, date = r
    try:
        DB.execute("""
            INSERT OR REPLACE INTO restrictions 
            (region, city, network, client_type, limit_type, limit_value, previous_value, source_url, source_date, is_current, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, datetime('now'))
        """, (region, city, network, client_type, limit_type, limit_value, prev, url, date))
        n += 1
    except Exception as e:
        print(f"Error inserting {region}: {e}")

DB.commit()
DB.close()
print(f"Inserted {n} restrictions")
