#!/usr/bin/env python3
"""Insert fresh restrictions for Aug 22, 2026"""
import sqlite3

restrictions = [
    # Калужская область - чет/нечет с 15 августа
    {"region": "Калужская область", "city": "", "network": "все сети", "customer_type": "все",
     "limit_type": "чет/нечет + запрет на канистры", "value": "четные/нечетные дни по номерам + только в бак",
     "url": "https://t.me/Shapsha_VV/19500", "date": "2026-08-15"},
    
    # Астраханская область - лимиты с 13 августа
    {"region": "Астраханская область", "city": "", "network": "Лукойл, Газпром", "customer_type": "все",
     "limit_type": "объем + график", "value": "40 л бензин, 60 л дизель в городе, 200 л дизель на трассе",
     "url": "https://www.sravni.ru/novost/2026/8/19/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", "date": "2026-08-13"},
    
    # Липецкая область - чет/нечет с 13 августа
    {"region": "Липецкая область", "city": "", "network": "Газпром, Лукойл, Teboil, Роснефть", "customer_type": "все",
     "limit_type": "чет/нечет + объем", "value": "четные/нечетные дни по номерам + 30 л бензин, дизель без ограничений",
     "url": "https://t.me/igor_artamonov48/7202", "date": "2026-08-13"},
    
    # Оренбургская область - чет/нечет с 12 августа
    {"region": "Оренбургская область", "city": "", "network": "все сети", "customer_type": "физлица и юрлица",
     "limit_type": "чет/нечет + объем", "value": "15-30 л бензин, 60 л дизель в городе, 200 л дизель на трассе",
     "url": "https://t.me/solntsev_official/5998", "date": "2026-08-12"},
    
    # Волгоградская область - лимиты с 1 августа
    {"region": "Волгоградская область", "city": "", "network": "Лукойл, Газпром", "customer_type": "все",
     "limit_type": "объем", "value": "40 л бензин, 60 л дизель в городе, 200 л дизель на трассе",
     "url": "https://tass.ru/ekonomika/27974231", "date": "2026-08-01"},
    
    # Иркутская область - лимиты с 13 августа
    {"region": "Иркутская область", "city": "", "network": "КрайсНефть", "customer_type": "физлица",
     "limit_type": "объем + канистры", "value": "30 л в бак, 20 л в канистры",
     "url": "https://www.interfax-russia.ru/siberia/news/nezavisimaya-set-azs-v-priangare-vvela-ogranicheniya-na-otpusk-topliva-dlya-fizlic", "date": "2026-08-13"},
    
    # Республика Алтай - смягчение с 11 августа
    {"region": "Республика Алтай", "city": "Горно-Алтайск", "network": "все сети", "customer_type": "все",
     "limit_type": "объем", "value": "50 л бензин, 100 л дизель (увеличено с 30/50)",
     "url": "https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/", "date": "2026-08-11"},
    
    # Тамбовская область - отмена чет/нечет на несетевых с 14 августа
    {"region": "Тамбовская область", "city": "", "network": "несетевые АЗС", "customer_type": "все",
     "limit_type": "отмена чет/нечет", "value": "отменена система чет/нечет, разрешены канистры",
     "url": "https://www.tambov.gov.ru/news/s-14-avgusta-na-nesetevyh-azs-v-tambovskoj-oblasti-otmenyayut-sistemu-chyot%E2%80%93nechet", "date": "2026-08-14"},
    
    # Тамбовская область - лимит на сетевых
    {"region": "Тамбовская область", "city": "", "network": "Роснефть, Лукойл", "customer_type": "все",
     "limit_type": "объем + чет/нечет", "value": "30 л бензин, действует чет/нечет",
     "url": "https://www.tambov.gov.ru/news/s-14-avgusta-na-nesetevyh-azs-v-tambovskoj-oblasti-otmenyayut-sistemu-chyot%E2%80%93nechet", "date": "2026-08-14"},
    
    # Москва - лимиты сетей
    {"region": "Москва", "city": "Москва", "network": "Газпромнефть", "customer_type": "все",
     "limit_type": "объем", "value": "60 л бензин",
     "url": "https://www.rbc.ru/economics/19/08/2026/6a84bb959a7947c0ad9b886f", "date": "2026-08-19"},
    
    {"region": "Москва", "city": "Москва", "network": "Татнефть", "customer_type": "все",
     "limit_type": "объем", "value": "50 л бензин, 60 л дизель",
     "url": "https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/", "date": "2026-08-19"},
]

db = sqlite3.connect('/root/diesel_limits/restrictions.db')
cur = db.cursor()

for r in restrictions:
    cur.execute('''
        INSERT OR IGNORE INTO restrictions(
            region, city, network, client_type, limit_type,
            limit_value, source_url, source_date, is_current, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, datetime('now'), datetime('now'))
    ''', (r["region"], r["city"], r["network"], r["customer_type"],
          r["limit_type"], r["value"], r["url"], r["date"]))

db.commit()
print(f"Inserted {len(restrictions)} restrictions")
db.close()
