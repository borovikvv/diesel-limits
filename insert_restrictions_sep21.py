#!/usr/bin/env python3
"""Insert diesel restrictions from Sep 2026 news (ponytail: minimal)."""
import sqlite3
from datetime import datetime
DB = "/root/diesel_limits/restrictions.db"
TODAY = "2026-09-21"
db = sqlite3.connect(DB)

# Restrictions from fresh news (July-Sep 2026)
# Format: (region, city, network, client_type, limit_type, value, url, date)
rows = [
    # From aa.com.tr (01.07.2026) + lenta.ru (07.07) + finance.mail.ru
    ("Республика Дагестан", None, "все АЗС", "физлица", "объем", "20 бенз / 50 дизель",
     "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-07-01"),
    ("Воронежская область", None, "Лукойл", "физлица", "объем", "30 бенз / 60 дизель (город), 60 бенз / 200 дизель (трасса)",
     "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-07-08"),
    ("Калининградская область", None, "все АЗС", "физлица", "объем", "30 бенз / 60 дизель",
     "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-07-01"),
    ("Республика Татарстан", None, "Газпромнефть", "все", "объем", "30 бенз / 60 дизель",
     "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-07-08"),
    ("Кировская область", "Киров", "Движение / Лукойл", "все", "объем", "30-100 бенз / 100 дизель",
     "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-07-08"),
    ("Мурманская область", None, "Лукойл", "все", "объем", "30 бенз / 60 дизель",
     "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-07-08"),
    ("Мурманская область", None, "Газпромнефть", "все", "объем", "30 бенз / 30 дизель (60 по карте)",
     "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-07-08"),
    ("Москва", None, "Газпромнефть", "все", "объем", "30 бенз / 60 дизель (город), до 200 дизель (трасса)",
     "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-07-08"),
    ("Москва", None, "Лукойл", "все", "объем", "20-30 без канистр",
     "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-07-08"),
    ("Вологодская область", None, "все АЗС", "физлица", "объем", "30 бенз / 60 дизель (город), 30 бенз / 200 дизель (трасса)",
     "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-07-08"),
    ("Красноярский край", None, "Газпромнефть", "все", "объем", "40 бенз, без канистр",
     "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-07-08"),
    ("Кемеровская область", None, "Газпромнефть", "все", "объем", "40 бенз / 80 дизель (200 трасса)",
     "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-07-08"),
    ("Омская область", None, "все АЗС", "физлица", "объем", "40 бенз / 80 дизель (город), 40 бенз / 200 дизель (трасса)",
     "https://www.svoboda.org/a/za-sutki-ogranicheniya-na-prodazhu-topliva-vveli-v-shesti-regionah-rossii/33786855.html", "2026-06-24"),
    ("Республика Алтай", "Горно-Алтайск", "все АЗС", "все", "объем", "50 бенз / 100 дизель (Чойский/Турочакский 30/50)",
     "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-07-09"),
    ("Томская область", None, "部分 AZS", "все", "объем", "30-40 бенз / 80 дизель",
     "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-07-08"),
    ("Владимирская область", None, "все АЗС", "физлица", "объем", "20-30 бенз / 40 дизель",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-09-01"),
    ("Якутия", None, "部分 AZS", "все", "объем", "30 бенз / 200 дизель, запрет тары",
     "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-07-01"),
    ("Брянская область", None, "все АЗС", "все", "запрет", "запрет продажи в канистры",
     "https://m.vk.ru/wall-65457623_44077", "2026-07-07"),
]

count = 0
for (region, city, network, client_type, limit_type, value, url, date) in rows:
    db.execute("""INSERT INTO restrictions 
        (region, city, network, client_type, limit_type, value, source_url, source_date, is_current, created_at, updated_at)
        VALUES (?,?,?,?,?,?,?,?,1,datetime('now'),datetime('now'))""",
        (region, city, network, client_type, limit_type, value, url, date))
    count += 1
db.commit()
db.close()
print(f"Inserted {count} restriction rows")
