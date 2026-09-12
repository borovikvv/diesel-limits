#!/usr/bin/env python3
"""Insert diesel restrictions from Jun-Aug 2026 news"""
import sqlite3
from datetime import datetime

db = sqlite3.connect('/root/diesel_limits/restrictions.db')
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Restrictions: (region, city, network, client_type, limit_type, limit_value, previous_value, source_url, source_date)
restrictions = [
    ("Калининградская область", "", "", "физлица", "объем", "60", None, "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-06-25"),
    ("Кемеровская область", "город", "", "физлица", "объем", "80", None, "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-06-23"),
    ("Кемеровская область", "трасса", "", "все", "объем", "200", None, "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-06-23"),
    ("Республика Дагестан", "", "", "физлица", "объем", "50", None, "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-06-25"),
    ("Владимирская область", "", "", "физлица", "объем", "40", None, "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-06-18"),
    ("Ивановская область", "", "", "физлица", "объем", "60", None, "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-02"),
    ("Республика Мордовия", "легковые", "", "физлица", "объем", "60", None, "https://news.mail.ru/economics/71391449/", "2026-06-23"),
    ("Республика Мордовия", "грузовые", "", "все", "объем", "300", None, "https://news.mail.ru/economics/71391449/", "2026-06-23"),
    ("Омская область", "город", "", "физлица", "объем", "80", None, "https://www.aa.com.tr/ru/%D1%8D%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0/%D0%B3%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F-%D0%BE%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D0%BD%D0%B8%D0%B9-%D0%BD%D0%B0-%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6%D1%83-%D1%82%D0%BE%D0%BF%D0%BB%D0%B8%D0%B2%D0%B0-%D0%B2-%D1%80%D0%BE%D1%81%D1%81%D0%B8%D0%B8-%D0%BF%D1%80%D0%BE%D0%B4%D0%BE%D0%BB%D0%B6%D0%B0%D0%B5%D1%82-%D1%80%D0%B0%D1%81%D1%88%D0%B8%D1%80%D1%8F%D1%82%D1%8C%D1%81%D1%8F/3983182", "2026-06-24"),
    ("Омская область", "трасса", "", "грузовые", "объем", "200", None, "https://www.aa.com.tr/ru/%D1%8D%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0/%D0%B3%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F-%D0%BE%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D0%BD%D0%B8%D0%B9-%D0%BD%D0%B0-%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6%D1%83-%D1%82%D0%BE%D0%BF%D0%BB%D0%B8%D0%B2%D0%B0-%D0%B2-%D1%80%D0%BE%D1%81%D1%81%D0%B8%D0%B8-%D0%BF%D1%80%D0%BE%D0%B4%D0%BE%D0%BB%D0%B6%D0%B0%D0%B5%D1%82-%D1%80%D0%B0%D1%81%D1%88%D0%B8%D1%80%D1%8F%D1%82%D1%8C%D1%81%D1%8F/3983182", "2026-06-24"),
    ("Тюменская область", "город", "Газпромнефть", "физлица", "объем", "80", None, "https://news.mail.ru/economics/71391449/", "2026-06-24"),
    ("Тюменская область", "трасса", "Газпромнефть", "все", "объем", "200", None, "https://news.mail.ru/economics/71391449/", "2026-06-24"),
    ("Мурманская область", "", "Лукойл", "физлица", "объем", "60", None, "https://www.aa.com.tr/ru/%D1%8D%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0/%D0%B3%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F-%D0%BE%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D0%BD%D0%B8%D0%B9-%D0%BD%D0%B0-%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6%D1%83-%D1%82%D0%BE%D0%BF%D0%BB%D0%B8%D0%B2%D0%B0-%D0%B2-%D1%80%D0%BE%D1%81%D1%81%D0%B8%D0%B8-%D0%BF%D1%80%D0%BE%D0%B4%D0%BE%D0%BB%D0%B6%D0%B0%D0%B5%D1%82-%D1%80%D0%B0%D1%81%D1%88%D0%B8%D1%80%D1%8F%D1%82%D1%8C%D1%81%D1%8F/3983182", "2026-06-24"),
    ("Республика Татарстан", "", "Татнефть", "физлица", "объем", "60", None, "https://www.e1.ru/text/transport/2026/06/18/76483435/", "2026-06-18"),
    ("Санкт-Петербург", "", "", "физлица", "объем", "60", None, "https://www.rbc.ru/economics/24/06/2026/6a3c13c59a7947597979e6a3", "2026-06-24"),
    ("Республика Саха (Якутия)", "", "", "физлица", "объем", "200", None, "https://www.aa.com.tr/ru/%D1%8D%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0/%D0%B3%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F-%D0%BE%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D0%BD%D0%B8%D0%B9-%D0%BD%D0%B0-%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6%D1%83-%D1%82%D0%BE%D0%BF%D0%BB%D0%B8%D0%B2%D0%B0-%D0%B2-%D1%80%D0%BE%D1%81%D1%81%D0%B8%D0%B8-%D0%BF%D1%80%D0%BE%D0%B4%D0%BE%D0%BB%D0%B6%D0%B0%D0%B5%D1%82-%D1%80%D0%B0%D1%81%D1%88%D0%B8%D1%80%D1%8F%D1%82%D1%8C%D1%81%D1%8F/3983182", "2026-07-01"),
    ("Воронежская область", "", "", "физлица", "объем", "60", None, "https://www.aa.com.tr/ru/%D1%8D%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0/%D0%B3%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F-%D0%BE%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D0%BD%D0%B8%D0%B9-%D0%BD%D0%B0-%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6%D1%83-%D1%82%D0%BE%D0%BF%D0%BB%D0%B8%D0%B2%D0%B0-%D0%B2-%D1%80%D0%BE%D1%81%D1%81%D0%B8%D0%B8-%D0%BF%D1%80%D0%BE%D0%B4%D0%BE%D0%BB%D0%B6%D0%B0%D0%B5%D1%82-%D1%80%D0%B0%D1%81%D1%88%D0%B8%D1%80%D1%8F%D1%82%D1%8C%D1%81%D1%8F/3983182", "2026-07-01"),
    ("Республика Карелия", "", "", "физлица", "объем", "60", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-06-28"),
    ("Кировская область", "", "", "физлица", "объем", "100", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Ульяновская область", "", "", "физлица", "объем", "100", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Республика Алтай", "", "", "физлица", "объем", "100", None, "https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/", "2026-08-19"),
    ("Москва", "", "", "физлица", "объем", "60", None, "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-08-19"),
    ("Москва", "трасса", "", "все", "объем", "200", None, "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-08-19"),
]

inserted = 0
for r in restrictions:
    region, city, network, client_type, limit_type, limit_value, prev, url, date = r
    db.execute("""
        INSERT INTO restrictions(
            region, city, network, client_type, limit_type, 
            limit_value, previous_value, source_url, source_date, 
            is_current, created_at, updated_at
        ) VALUES(?,?,?,?,?,?,?, ?,?,1,?,?)
    """, (region, city, network, client_type, limit_type, 
          limit_value, prev, url, date, now, now))
    inserted += 1

db.commit()
db.close()
print(f"Inserted {inserted} new diesel restrictions")
