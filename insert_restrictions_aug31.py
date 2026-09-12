import sqlite3
from datetime import datetime

# Свежие ограничения на 31 августа 2026 (из sravni.ru, lenta.ru, aa.com.tr)
restrictions = [
    # Регион, город, сеть, тип_клиента, тип_лимита, значение, URL, дата
    ("Астраханская область", None, None, "все", "объем+чет-нечет", "30 л бензина АИ-92/АИ-95, чет/нечет по номерам", "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-31"),
    ("Республика Алтай", None, None, "все", "объем+суточный", "50 л бензина, 100 л дизеля в сутки, до 1 сентября", "https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/", "2026-08-31"),
    ("Владимирская область", None, None, "все", "время+объем", "7:00-10:00 только экстренные службы, 20-30 л бензина, 40 л дизеля", "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-31"),
    ("Калужская область", None, None, "все", "чет-нечет", "чет/нечет по номерам, только в бак, не на дизель", "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-31"),
    ("Курская область", None, None, "все", "объем+чет-нечет", "30-50 л, чет/нечет по номерам", "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-31"),
    ("Липецкая область", None, None, "все", "объем+чет-нечет", "30 л бензина, чет/нечет, на дизель нет", "https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/", "2026-08-31"),
    ("Мордовия", None, None, "все", "объем+чет-нечет", "40 л бензина, 60 л дизеля легковые, 300 л грузовые, чет/нечет", "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-31"),
    ("Нижегородская область", None, None, "все", "объем+чет-нечет", "30-60 л бензина, чет/нечет по номерам", "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-31"),
    ("Новосибирская область", None, None, "все", "объем+возраст", "30 л бензина, 60 л дизеля, запрет до 18 лет (исключение 16+ с правами)", "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-31"),
    ("Оренбургская область", None, None, "все", "объем+чет-нечет", "15-30 л бензина, 60 л дизеля город, 200 л трасса, чет/нечет", "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-31"),
    ("Тамбовская область", None, None, "все", "объем+чет-нечет", "30 л бензина, чет/нечет только сетевые АЗС", "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-31"),
    ("Новгородская область", None, None, "все", "возраст", "с 1 сентября запрет до 18 лет (исключение 16+ с правами)", "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-31"),
    ("Крым", None, None, "все", "QR+объем", "20 л бензина по QR-кодам, 40 л дизеля свободно, только бак", "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-31"),
    ("Севастополь", None, None, "все", "QR+объем", "20 л бензина по QR-кодам, 40 л дизеля свободно, только бак", "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-31"),
    ("Магаданская область", "Магадан", None, "все", "объем", "100 л бензина в сутки, 500 л дизеля в городе, 250 л в области", "https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/", "2026-08-31"),
]

db = sqlite3.connect('/root/diesel_limits/restrictions.db')
inserted = 0
for r in restrictions:
    try:
        db.execute('''INSERT INTO restrictions(
            region,city,network,client_type,limit_type,
            limit_value,source_url,source_date,is_current
        ) VALUES(?,?,?,?,?,?,?,?,1)''',
        (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))
        inserted += 1
    except Exception as e:
        print(f"Error {r[0]}: {e}")

db.commit()
print(f"Inserted {inserted} restrictions")
db.close()
