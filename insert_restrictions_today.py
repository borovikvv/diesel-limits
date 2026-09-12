import sqlite3
from datetime import datetime

db = sqlite3.connect('restrictions.db')
today = "2026-08-27"

# Restrictions from search results (sravni, lenta, aa.com.tr, benzinmap)
restrictions = [
    # Дагестан
    ("Республика Дагестан", None, None, "физлица", "объем", "20 л бензин, 50 л дизель, только в бак", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", today),
    
    # Владимирская область
    ("Владимирская область", None, None, "физлица", "объем", "20-30 л бензин, до 40 л дизель", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", today),
    
    # Ивановская область
    ("Ивановская область", None, None, "физлица", "объем", "30 л бензин, 60 л дизель, только в бак", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", today),
    
    # Кемеровская область
    ("Кемеровская область", None, "Газпромнефть", "физлица", "объем", "40 л бензин, 80 л дизель город, 200 л трасса", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", today),
    
    # Москва
    ("Москва", None, "Газпромнефть", "физлица", "объем", "60 л дизель город, 200 л трасса", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", today),
    ("Москва", None, "Лукойл", "физлица", "объем", "20-30 л бензин, 60 л дизель", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", today),
    
    # Приморский край
    ("Приморский край", None, None, "грузовики", "объем", "100 л дизель город, 200 л трасса", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", today),
    
    # Краснодарский край
    ("Краснодарский край", "Анапа", None, "все", "объем", "20-30 л бензин, 30-60 л дизель", None, "https://benzinmap.ru/", today),
    
    # Псковская область
    ("Псковская область", None, None, "физлица", "объем", "40 л дизель", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", today),
    
    # Удмуртия
    ("Удмуртская Республика", None, None, "физлица", "объем", "40 л бензин, 60 л дизель легковые, 250 л грузовые", None, "https://benzinmap.ru/", today),
    
    # Калининградская область
    ("Калининградская область", None, "Лукойл", "все", "снято", "без ограничений", "30 л бензин, 60 л дизель", "https://benzinmap.ru/", today),
    ("Калининградская область", None, "Сургутнефтегаз", "все", "снято", "без ограничений", "30 л бензин, 60 л дизель", "https://benzinmap.ru/", today),
    ("Калининградская область", None, None, "физлица", "объем", "30 л бензин, 60 л дизель", None, "https://www.aa.com.tr/ru/economics/geography-fuel-restrictions/3983182", today),
    
    # Нижегородская область
    ("Нижегородская область", None, "Газпромнефть", "все", "снято", "без ограничений", None, "https://benzinmap.ru/", today),
    
    # Вологодская область
    ("Вологодская область", None, "Лукойл", "физлица", "объем", "60 л дизель город, 200 л трасса", None, "https://benzinmap.ru/", today),
    ("Вологодская область", None, "Газпромнефть", "все", "снято", "без ограничений", None, "https://benzinmap.ru/", today),
    
    # Мурманская область
    ("Мурманская область", None, "Лукойл", "физлица", "объем", "60 л дизель", None, "https://benzinmap.ru/", today),
    
    # Ярославская область
    ("Ярославская область", None, None, "физлица", "объем", "30 л бензин, 60 л дизель", None, "https://benzinmap.ru/", today),
    
    # Белгородская область
    ("Белгородская область", None, "Роснефть", "физлица", "запрет", "запрет заправки в канистры", None, "https://benzinmap.ru/", today),
    ("Белгородская область", None, "Газпромнефть", "физлица", "объем", "60 л дизель", None, "https://benzinmap.ru/", today),
    
    # Иркутская область
    ("Иркутская область", None, "Роснефть", "физлица", "объем", "50 л в сутки, запрет в канистры", None, "https://benzinmap.ru/", today),
    
    # Забайкальский край
    ("Забайкальский край", "Чита", "Корс", "физлица", "снято", "без ограничений", "20 л бензин", "https://benzinmap.ru/", today),
    ("Забайкальский край", "Чита", "БРК", "физлица", "снято", "без ограничений", "20 л бензин", "https://benzinmap.ru/", today),
    ("Забайкальский край", None, "Балтнефть", "физлица", "объем", "30 л бензин, 100 л дизель", None, "https://benzinmap.ru/", today),
    
    # Воронежская область
    ("Воронежская область", None, "Лукойл", "все", "объем", "30 л бензин, 60 л дизель город, 200 л трасса", None, "https://www.aa.com.tr/ru/economics/geography-fuel-restrictions/3983182", today),
    
    # Омская область
    ("Омская область", None, None, "физлица", "объем", "40 л бензин, 80 л дизель город, 200 л трасса", None, "https://www.aa.com.tr/ru/economics/geography-fuel-restrictions/3983182", today),
    
    # Якутия
    ("Республика Саха (Якутия)", None, "Саханефтегазсбыт", "все", "объем", "30 л бензин, 200 л дизель, запрет в тару", None, "https://www.aa.com.tr/ru/economics/geography-fuel-restrictions/3983182", today),
    
    # Пензенская область
    ("Пензенская область", None, None, "физлица", "объем", "100 л бензин, 200 л дизель", None, "https://www.aa.com.tr/ru/economics/geography-fuel-restrictions/3983182", today),
    
    # Республика Алтай
    ("Республика Алтай", "Горно-Алтайск", None, "физлица", "объем", "30 л бензин, 50 л дизель", None, "https://benzinmap.ru/", today),
    ("Республика Алтай", "Майминский район", None, "физлица", "объем", "30 л бензин, 50 л дизель", None, "https://benzinmap.ru/", today),
    ("Республика Алтай", "Чемальский район", None, "физлица", "объем", "30 л бензин, 50 л дизель", None, "https://benzinmap.ru/", today),
    ("Республика Алтай", None, None, "физлица", "объем", "50 л бензин, 100 л дизель остальные районы", None, "https://benzinmap.ru/", today),
    
    # Астраханская область
    ("Астраханская область", None, None, "физлица", "объем", "40 л бензин", None, "https://benzinmap.ru/", today),
    
    # Магаданская область
    ("Магаданская область", "Магадан", None, "все", "объем", "100 л бензин, 500 л дизель", None, "https://benzinmap.ru/", today),
    ("Магаданская область", None, None, "все", "объем", "100 л бензин, 250 л дизель остальные территории", None, "https://benzinmap.ru/", today),
    
    # Ставропольский край
    ("Ставропольский край", None, None, "физлица", "объем", "30 л бензин, 60 л дизель", None, "https://benzinmap.ru/", today),
    
    # Ненецкий АО
    ("Ненецкий АО", None, "Лукойл", "физлица", "объем", "20 л бензин, 60 л дизель", None, "https://benzinmap.ru/", today),
    ("Ненецкий АО", None, "Ненецкая нефтяная компания", "физлица", "объем", "20 л бензин, 60 л дизель", None, "https://benzinmap.ru/", today),
    
    # Ямало-Ненецкий АО
    ("Ямало-Ненецкий АО", None, "Лукойл", "все", "объем", "40 л бензин, 60 л дизель легковые, 300 л грузовые, запрет в тару", None, "https://benzinmap.ru/", today),
    
    # Татарстан
    ("Республика Татарстан", None, "Татнефть", "физлица", "объем", "30 л АИ-95, 60 л дизель легковые, 300 л грузовые", None, "https://www.aa.com.tr/ru/economics/geography-fuel-restrictions/3983182", today),
    ("Республика Татарстан", None, "Газпромнефть", "физлица", "объем", "30 л бензин, 60 л дизель", None, "https://www.aa.com.tr/ru/economics/geography-fuel-restrictions/3983182", today),
    
    # Кировская область
    ("Кировская область", None, "Лукойл", "физлица", "объем", "30 л бензин, 60 л дизель", None, "https://www.aa.com.tr/ru/economics/geography-fuel-restrictions/3983182", today),
    
    # Мордовия
    ("Республика Мордовия", None, None, "физлица", "объем", "30 л бензин", None, "https://ru.wikipedia.org/wiki/Fuel_crisis_in_Russia_2025", today),
    
    # Липецкая область
    ("Липецкая область", None, None, "физлица", "объем", "30 л бензин", None, "https://ru.wikipedia.org/wiki/Fuel_crisis_in_Russia_2025", today),
    
    # Саратовская область
    ("Саратовская область", None, None, "физлица", "объем", "30 л бензин", None, "https://ru.wikipedia.org/wiki/Fuel_crisis_in_Russia_2025", today),
]

# Build existing index
existing = {}
for row in db.execute("SELECT id, region, network, client_type, limit_type, limit_value, previous_value, is_current FROM restrictions"):
    key = (row[1], row[2] or '', row[3] or '', row[4] or '')
    existing[key] = row

count_new = 0
count_updated = 0

for r in restrictions:
    region, city, network, client_type, limit_type, limit_value, previous_value, source_url, source_date = r
    key = (region, network or '', client_type or '', limit_type or '')
    
    if key in existing:
        rid, _, _, _, _, old_val, old_prev, old_current = existing[key]
        if old_val != limit_value:
            # UPDATE
            db.execute(
                "UPDATE restrictions SET limit_value=?, previous_value=?, source_url=?, source_date=?, is_current=1 WHERE id=?",
                (limit_value, previous_value or old_prev, source_url, source_date, rid)
            )
            count_updated += 1
    else:
        # INSERT
        db.execute(
            "INSERT INTO restrictions(region,city,network,client_type,limit_type,limit_value,previous_value,source_url,source_date,is_current,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,datetime('now'))",
            (region, city, network, client_type, limit_type, limit_value, previous_value, source_url, source_date, 1)
        )
        count_new += 1

db.commit()
db.close()
print(f"Restrictions: {count_new} new, {count_updated} updated")
