#!/usr/bin/env python3
"""Insert fresh September 2026 diesel restrictions."""
import sqlite3

db = sqlite3.connect('/root/diesel_limits/restrictions.db')
today = '2026-09-19'

new_restr = [
    ("Ленинградская область", None, None, "физлица", "объем", "30 л", None,
     "https://ura.news/articles/1053127702", today),
    ("Ямало-Ненецкий АО", None, None, "физлица", "объем", "лимиты на бензин, дизель свободно", None,
     "https://ura.news/articles/1053127702", today),
    ("Республика Дагестан", "Махачкала", None, "все", "объем", "20 л бенз / 50 л диз", None,
     "https://www.sravni.ru/novost/2026/9/9/toplivo-v-rossii-situacziya-na-utro-9-sentyabrya-2026/", today),
    ("Челябинская область", "Челябинск", None, "все", "контроль", "ручной режим поставок", None,
     "https://ura.news/articles/1053127702", today),
    ("Свердловская область", "Екатеринбург", None, "все", "контроль", "ручной режим поставок", None,
     "https://ura.news/articles/1053127702", today),
    ("Приморский край", None, None, "все", "запрет", "только в бак", None,
     "https://www.sravni.ru/novost/2026/8/26/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "2026-08-26"),
]

ins = 0
for r in new_restr:
    db.execute("""INSERT INTO restrictions
        (region, city, network, client_type, limit_type, limit_value, previous_value,
         source_url, source_date, is_current, created_at, updated_at)
        VALUES (?,?,?,?,?,?,?, ?,?, 1, datetime('now'), datetime('now'))""", r)
    ins += 1

db.commit()
print(f"Inserted {ins} new restriction records")
db.close()
