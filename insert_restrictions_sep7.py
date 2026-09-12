#!/usr/bin/env python3
"""Insert fresh diesel restrictions from web searches."""
import sqlite3, datetime

restrictions = [
    # Дагестан
    {"region": "Республика Дагестан", "city": None, "network": "все АЗС", "client_type": "физлица", 
     "limit_type": "объем", "value": "20 л бензин, 50 л дизель", "url": "https://news.mail.ru/economics/71391449/", "date": "2026-06-24"},
    
    # Воронежская область
    {"region": "Воронежская область", "city": None, "network": "все АЗС", "client_type": "все",
     "limit_type": "объем", "value": "30 л бензин, 60 л дизель", "url": "https://finance.mail.ru/article/30-litrov-na-avto-v-kakih-regionah-vveli-ogranicheniya-iz-za-toplivnogo-krizisa-69214349/", "date": "2026-06-23"},
    
    # Омская область
    {"region": "Омская область", "city": None, "network": "все АЗС", "client_type": "все",
     "limit_type": "объем", "value": "40 л бензин, 80 л дизель; на трассах: 40 л бензин, 200 л дизель", "url": "https://news.mail.ru/economics/71391449/", "date": "2026-06-24"},
    
    # Калининградская область
    {"region": "Калининградская область", "city": None, "network": "все АЗС", "client_type": "все",
     "limit_type": "объем", "value": "30 л бензин, 60 л дизель", "url": "https://www.aa.com.tr/ru/%D1%8D%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0/%D0%B3%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F-%D0%BE%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D0%BD%D0%B8%D0%B9-%D0%BD%D0%B0-%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6%D1%83-%D1%82%D0%BE%D0%BF%D0%BB%D0%B8%D0%B2%D0%B0-%D0%B2-%D1%80%D0%BE%D1%81%D1%81%D0%B8%D0%B8-%D0%BF%D1%80%D0%BE%D0%B4%D0%BE%D0%BB%D0%B6%D0%B0%D0%B5%D1%82-%D1%80%D0%B0%D1%81%D1%88%D0%B8%D1%80%D1%8F%D1%82%D1%8C%D1%81%D1%8F/3983182", "date": "2026-07-01"},
    
    # Татарстан
    {"region": "Республика Татарстан", "city": None, "network": "Газпромнефть", "client_type": "все",
     "limit_type": "объем", "value": "30 л бензин, 60 л дизель", "url": "https://finance.mail.ru/article/30-litrov-na-avto-v-kakih-regionah-vveli-ogranicheniya-iz-za-toplivnogo-krizisa-69214349/", "date": "2026-06-24"},
    
    # Мурманская область
    {"region": "Мурманская область", "city": None, "network": "Лукойл", "client_type": "все",
     "limit_type": "объем", "value": "30 л бензин, 60 л дизель", "url": "https://finance.mail.ru/article/30-litrov-na-avto-v-kakih-regionah-vveli-ogranicheniya-iz-za-toplivnogo-krizisa-69214349/", "date": "2026-06-24"},
    
    # Мурманская область - Газпромнефть
    {"region": "Мурманская область", "city": None, "network": "Газпромнефть", "client_type": "все",
     "limit_type": "объем", "value": "30 л бензин, 30 л дизель (60 л по карте лояльности)", "url": "https://finance.mail.ru/article/30-litrov-na-avto-v-kakih-regionah-vveli-ogranicheniya-iz-za-toplivnogo-krizisa-69214349/", "date": "2026-06-24"},
    
    # Кемеровская область
    {"region": "Кемеровская область", "city": None, "network": "Газпромнефть", "client_type": "все",
     "limit_type": "объем", "value": "40 л бензин, 80 л дизель; на трассах: до 200 л дизель", "url": "https://www.aa.com.tr/ru/%D1%8D%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0/%D0%B3%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F-%D0%BE%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D0%BD%D0%B8%D0%B9-%D0%BD%D0%B0-%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6%D1%83-%D1%82%D0%BE%D0%BF%D0%BB%D0%B8%D0%B2%D0%B0-%D0%B2-%D1%80%D0%BE%D1%81%D1%81%D0%B8%D0%B8-%D0%BF%D1%80%D0%BE%D0%B4%D0%BE%D0%BB%D0%B6%D0%B0%D0%B5%D1%82-%D1%80%D0%B0%D1%81%D1%88%D0%B8%D1%80%D1%8F%D1%82%D1%8C%D1%81%D1%8F/3983182", "date": "2026-07-01"},
    
    # Красноярский край
    {"region": "Красноярский край", "city": None, "network": "Газпромнефть", "client_type": "все",
     "limit_type": "объем", "value": "40 л бензин, канистры запрещены", "url": "https://finance.mail.ru/article/30-litrov-na-avto-v-kakih-regionah-vveli-ogranicheniya-iz-za-toplivnogo-krizisa-69214349/", "date": "2026-06-24"},
    
    # Вологодская область
    {"region": "Вологодская область", "city": None, "network": "все АЗС", "client_type": "все",
     "limit_type": "объем", "value": "30 л бензин, 60 л дизель; на трассах: 30 л бензин, 200 л дизель", "url": "https://finance.mail.ru/article/30-litrov-na-avto-v-kakih-regionah-vveli-ogranicheniya-iz-za-toplivnogo-krizisa-69214349/", "date": "2026-06-24"},
    
    # Кировская область
    {"region": "Кировская область", "city": None, "network": "Движение", "client_type": "все",
     "limit_type": "объем", "value": "30 л бензин 92/95, 100 л дизель", "url": "https://finance.mail.ru/article/30-litrov-na-avto-v-kakih-regionah-vveli-ogranicheniya-iz-za-toplivnogo-krizisa-69214349/", "date": "2026-06-24"},
    
    # Кировская область - Лукойл
    {"region": "Кировская область", "city": None, "network": "Лукойл", "client_type": "все",
     "limit_type": "объем", "value": "100 л бензин 92/95", "url": "https://finance.mail.ru/article/30-litrov-na-avto-v-kakih-regionah-vveli-ogranicheniya-iz-za-toplivnogo-krizisa-69214349/", "date": "2026-06-24"},
    
    # Якутия
    {"region": "Республика Саха (Якутия)", "city": None, "network": "некоторые АЗС", "client_type": "все",
     "limit_type": "объем", "value": "30 л бензин, 200 л дизель, канистры запрещены", "url": "https://www.aa.com.tr/ru/%D1%8D%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0/%D0%B3%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F-%D0%BE%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D0%BD%D0%B8%D0%B9-%D0%BD%D0%B0-%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6%D1%83-%D1%82%D0%BE%D0%BF%D0%BB%D0%B8%D0%B2%D0%B0-%D0%B2-%D1%80%D0%BE%D1%81%D1%81%D0%B8%D0%B8-%D0%BF%D1%80%D0%BE%D0%B4%D0%BE%D0%BB%D0%B6%D0%B0%D0%B5%D1%82-%D1%80%D0%B0%D1%81%D1%88%D0%B8%D1%80%D1%8F%D1%82%D1%8C%D1%81%D1%8F/3983182", "date": "2026-07-01"},
    
    # Брянская область
    {"region": "Брянская область", "city": None, "network": "все АЗС", "client_type": "физлица",
     "limit_type": "запрет", "value": "запрет продажи в канистры", "url": "https://vk.ru/wall-65457623_44077", "date": "2026-07-07"},
    
    # Общие ограничения по РФ
    {"region": "Россия", "city": None, "network": "все АЗС", "client_type": "физлица",
     "limit_type": "объем", "value": "100 л бензин, 200 л дизель на ТС", "url": "https://www.svoboda.org/a/za-sutki-ogranicheniya-na-prodazhu-topliva-vveli-v-shesti-regionah-rossii/33786855.html", "date": "2026-06-24"},
]

db = sqlite3.connect('/root/diesel_limits/restrictions.db')

for r in restrictions:
    db.execute('''INSERT OR REPLACE INTO restrictions 
                  (region, city, network, client_type, limit_type, limit_value, source_url, source_date, is_current)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)''',
               (r['region'], r['city'], r['network'], r['client_type'], r['limit_type'], r['value'], r['url'], r['date']))

db.commit()
print(f'Inserted {len(restrictions)} restriction rows')
db.close()
