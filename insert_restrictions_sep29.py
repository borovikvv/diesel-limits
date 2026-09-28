#!/usr/bin/env python3
"""Insert fresh diesel restrictions from search results (sep 2026)."""
import sqlite3

db = sqlite3.connect('/root/diesel_limits/restrictions.db')

# Restrictions from mail.ru, lenta.ru, vk sources (june-sep 2026)
# Format: (region, city, station_chain, client_type, restriction_type, value, url, date)
restrictions = [
    # Воронежская область
    ("Воронежская область", None, "сетевые АЗС", "физлица", "объем", "60л в городе, 200л на трассе",
     "https://news.mail.ru/economics/71391449/", "2026-09-29"),
    # Омская область
    ("Омская область", None, "все АЗС", "физлица", "объем", "80л в городе, 200л на трассе",
     "https://news.mail.ru/economics/71391449/", "2026-09-29"),
    # Самарская область
    ("Самарская область", None, "все АЗС", "физлица", "объем", "100л для легковых",
     "https://news.mail.ru/economics/71391449/", "2026-09-29"),
    # Краснодарский край
    ("Краснодарский край", None, "разные АЗС", "физлица", "объем", "30-60л дизель",
     "https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/", "2026-09-29"),
    # Приморский край
    ("Приморский край", None, "все АЗС", "юридические", "объем", "100л город, 200л трасса для большегрузов",
     "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-09-29"),
    # Кировская область
    ("Кировская область", None, "АЗС Движение", "все", "объем", "100л дизель",
     "https://m.vk.ru/wall-65457623_44077", "2026-09-29"),
    # Республика Татарстан
    ("Республика Татарстан", None, "Татнефть", "физлица", "объем", "60л дизель",
     "https://m.vk.ru/wall-65457623_44077", "2026-09-29"),
    # Красноярский край
    ("Красноярский край", None, "Газпромнефть", "физлица", "объем", "200л дизель",
     "https://m.vk.ru/wall-65457623_44077", "2026-09-29"),
    # Кемеровская область
    ("Кемеровская область", None, "все АЗС", "физлица", "объем", "80л дизель, 200л на трассе",
     "https://news.mail.ru/economics/71391449/", "2026-09-29"),
    # Белгородская область
    ("Белгородская область", None, "Лукойл", "физлица", "объем", "60л дизель",
     "https://news.mail.ru/economics/71391449/", "2026-09-29"),
    # Томская область
    ("Томская область", "Колпашевский, Асиновский, Зырянский, Тегульдетский районы", "все АЗС", "физлица", "объем", "80л дизель",
     "https://m.vk.ru/wall-65457623_44077", "2026-09-29"),
    # Вологодская область
    ("Вологодская область", None, "все АЗС", "физлица", "объем", "200л дизель на трассе, 60л в городе",
     "https://m.vk.ru/wall-65457623_44077", "2026-09-29"),
    # Ханты-Мансийский АО
    ("Ханты-Мансийский АО", None, "Газпромнефть", "физлица", "объем", "80л дизель",
     "https://m.vk.ru/wall-65457623_44077", "2026-09-29"),
    # Ростовская область
    ("Ростовская область", None, "все АЗС", "физлица", "объем", "40л на автомобиль",
     "https://m.vk.ru/wall-65457623_44077", "2026-09-29"),
    # Ставропольский край
    ("Ставропольский край", None, "все АЗС", "физлица", "объем", "35л на легковой",
     "https://m.vk.ru/wall-65457623_44077", "2026-09-29"),
    # Республика Дагестан
    ("Республика Дагестан", None, "все АЗС", "физлица", "объем", "50л дизель",
     "https://m.vk.ru/wall-65457623_44077", "2026-09-29"),
    # Тамбовская область
    ("Тамбовская область", None, "все АЗС", "все", "запрет", "запрет продажи в канистры",
     "https://news.mail.ru/economics/71391449/", "2026-09-29"),
    # Ульяновская область
    ("Ульяновская область", None, "некоторые АЗС", "все", "объем", "100л дизель",
     "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-09-29"),
]

# Mark old restrictions from these regions as not current
regions_updated = set(r[0] for r in restrictions)
for region in regions_updated:
    db.execute('UPDATE restrictions SET is_current=0 WHERE region=? AND is_current=1', (region,))

# Insert new restrictions
count = 0
for region, city, station, client, rtype, value, url, date in restrictions:
    db.execute('''
        INSERT OR REPLACE INTO restrictions(region,city,network,client_type,limit_type,
            limit_value,source_url,source_date,is_current)
        VALUES(?,?,?,?,?,?,?,?,1)
    ''', (region, city, station, client, rtype, value, url, date))
    count += 1

db.commit()
db.close()
print(f"Inserted {count} diesel restrictions for {len(regions_updated)} regions")
