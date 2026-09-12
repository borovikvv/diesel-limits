#!/usr/bin/env python3
"""Insert fresh diesel restrictions — simple INSERT OR REPLACE."""
import sqlite3
from datetime import datetime

DB = "/root/diesel_limits/restrictions.db"
SRC_DATE = "2026-07-28"
SRC_UPDATED = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

new_restrictions = [
    ("Москва", None, "Газпромнефть", "физлица", "объем", "до 30 л бензина, 60 л дизеля; на трассах до 200 л дизеля", "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/"),
    ("Москва", None, "Лукойл", "физлица", "объем", "20-30 л топлива на клиента", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Республика Крым", None, None, "все", "запрет", "свободная продажа топлива приостановлена; заправка только для спецслужб", "https://zona.media/article/2026/06/26/fuel-limit"),
    ("город федерального значения Севастополь", None, None, "физлица", "объем", "20 л бензина, АИ-92 30-40 л; дизель свободно", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Республика Дагестан", None, None, "физлица", "объем", "до 20 л бензина, 50 л дизеля", "https://tass.ru/obschestvo/27855585"),
    ("Владимирская область", None, None, "физлица", "объем", "20-30 л бензина, до 40 л дизеля", "https://vladtv.ru/society/172950/"),
    ("Ивановская область", None, None, "физлица", "объем", "до 30 л бензина, 60-200 л дизеля", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Кемеровская область", None, "Газпромнефть/Лукойл", "физлица", "объем", "до 40 л бензина, 80 л дизеля; трассы до 200 л дизеля", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm"),
    ("Омская область", None, None, "физлица", "объем", "до 40 л бензина, 80 л дизеля; трассы до 200 л дизеля", "https://www.kommersant.ru/doc/8763676"),
    ("Вологодская область", None, "Лукойл", "физлица", "объем", "до 30 л бензина, 60 л дизеля; трассы до 200 л дизеля", "https://www.kommersant.ru/doc/8763676"),
    ("Приморский край", None, None, "юрлица/грузовики", "объем", "до 100 л дизеля (город), до 200 л (трасса)", "https://primorsky.ru/news/318665"),
    ("Белгородская область", None, "Лукойл", "физлица", "объем", "до 30 л бензина, 60 л дизеля", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/"),
    ("Самарская область", None, None, "физлица", "объем", "до 40 л бензина, 100 л дизеля; грузовики до 300 л дизеля", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Ульяновская область", None, None, "физлица", "объем", "до 40 л бензина, 100 л дизеля; грузовики до 300 л", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Пензенская область", None, None, "физлица", "объем", "до 100 л бензина, 200 л дизеля", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Ростовская область", None, None, "физлица", "объем", "до 30 л бензина, 60 л дизеля; грузовики до 200 л, автобусы до 300 л", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Республика Татарстан", None, "Татнефть", "физлица", "объем", "до 30 л бензина, 60 л дизеля; грузовики до 300 л; топливные карты без лимита", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Чувашская Республика", None, None, "физлица", "объем", "до 30 л бензина; 300 л дизеля для грузовиков", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Республика Саха (Якутия)", None, "Саханефтегазсбыт", "физлица", "объем", "до 30 л бензина, до 200 л дизеля; запрет на канистры", "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/"),
    ("Республика Алтай", None, None, "физлица", "объем", "Горно-Алтайск: 30/50 л; остальные: 50/100 л; канистры до 10 л", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Тюменская область", None, "Газпромнефть", "физлица", "объем", "до 40 л бензина, 80 л дизеля (город), до 200 л (трасса)", "https://www.kommersant.ru/doc/8763676"),
    ("Курганская область", None, None, "физлица", "объем", "до 40 л бензина, 80 л дизеля (город), до 200 л (трасса)", "https://www.kommersant.ru/doc/8763676"),
    ("Мурманская область", None, "Лукойл", "физлица", "объем", "до 30 л бензина, 60 л дизеля", "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/"),
    ("Мурманская область", None, "Роснефть", "физлица", "объем", "до 99 л бензина, дизель без ограничений", "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/"),
    ("Мурманская область", None, "Газпромнефть", "физлица", "объем", "до 30 л бензина и дизеля; по карте до 60 л дизеля", "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/"),
    ("Воронежская область", None, "Лукойл", "физлица", "объем", "до 30 л бензина, 60 л дизеля (город); трассы 60/200 л", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Калининградская область", None, None, "физлица", "объем", "до 30 л бензина, 60 л дизеля", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Краснодарский край", None, None, "физлица", "объем", "20-30 л бензина, 30-60 л дизеля", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/"),
    ("Астраханская область", None, None, "физлица", "время", "заправка по четным/нечетным номерам машин", "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/"),
    ("Нижегородская область", None, None, "физлица", "объем", "до 40 л топлива; тест QR-кодов; заправка по дням", "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/"),
    ("Липецкая область", None, None, "физлица", "объем", "до 30 л бензина; заправка по номерам 11.07-01.08", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Забайкальский край", None, None, "физлица", "объем", "до 15 л бензина; только в бак; QR-коды", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Новосибирская область", None, None, "физлица", "объем", "до 30 л бензина, 60 л дизеля", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Республика Карелия", None, None, "физлица", "объем", "до 30 л бензина, 60 л дизеля; грузовики до 250 л дизеля", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Томская область", None, None, "физлица", "объем", "30-40 л бензина, 80 л дизеля", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Республика Мордовия", None, None, "физлица", "объем", "20/60 л легковые, 300 л грузовые; заправка по номерам", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Орловская область", None, None, "физлица", "объем", "до 30 л бензина; дизель без ограничений", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Саратовская область", None, None, "физлица", "объем", "до 30 л бензина", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/"),
    ("Челябинская область", None, "Татнефть", "физлица", "объем", "30 л бензина, 60 л дизеля", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Тамбовская область", None, None, "физлица", "объем", "до 30 л бензина; Роснефть АИ-92 без лимита", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Псковская область", None, None, "физлица", "объем", "до 40 л дизеля", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/"),
    ("Удмуртская Республика", None, None, "физлица", "объем", "до 40 л дизеля", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/"),
    ("Кировская область", None, None, "физлица", "объем", "до 100 л на некоторых АЗС; заправка по номерам", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Свердловская область", None, "Газпромнефть", "физлица", "объем", "до 40 л бензина и дизеля", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Волгоградская область", None, "Лукойл", "физлица", "объем", "до 30 л бензина за транзакцию", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Республика Башкортостан", None, None, "физлица", "объем", "до 30 л бензина", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Республика Калмыкия", None, None, "физлица", "объем", "до 30 л бензина", "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Ханты-Мансийский автономный округ", None, None, "физлица", "объем", "60-80 л дизеля на АЗС", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/"),
    ("Российская Федерация", None, None, "все", "запрет", "полный запрет экспорта дизельного топлива до 31 июля 2026", "https://novayagazeta.ru/articles/2026/07/13/menshe-ezdit-budete"),
    ("Российская Федерация", None, None, "все", "другое", "постановление №819: разрешен выпуск дизеля с серой до 350 мг/кг", "https://novayagazeta.ru/articles/2026/07/13/menshe-ezdit-budete"),
]

db = sqlite3.connect(DB)
inserted, updated = 0, 0
for r in new_restrictions:
    region, city, network, client_type, limit_type, limit_value, source_url = r
    
    # Check if row already exists with same key
    existing = db.execute(
        "SELECT id, limit_value FROM restrictions WHERE region=? AND network IS ? AND client_type=? AND limit_type=?",
        (region, network, client_type, limit_type)
    ).fetchone()
    
    if existing:
        if existing[1] != limit_value:
            # Update existing row in-place since UNIQUE prevents dups
            db.execute(
                "UPDATE restrictions SET city=?, limit_value=?, previous_value=?, source_url=?, source_date=?, is_current=1, updated_at=? WHERE id=?",
                (city, limit_value, existing[1], source_url, SRC_DATE, SRC_UPDATED, existing[0])
            )
            updated += 1
        # else: same value, skip
    else:
        db.execute(
            "INSERT INTO restrictions(region,city,network,client_type,limit_type,limit_value,previous_value,source_url,source_date,is_current,created_at,updated_at) "
            "VALUES(?,?,?,?,?,?,?,?,?,1,?,?)",
            (region, city, network, client_type, limit_type, limit_value, limit_value, source_url, SRC_DATE, SRC_UPDATED, SRC_UPDATED)
        )
        inserted += 1

db.commit()
print(f"Inserted {inserted} new, updated {updated} changed")
print(f"Active restrictions: {db.execute('SELECT COUNT(*) FROM restrictions WHERE is_current=1').fetchone()[0]}")
print(f"Total restrictions: {db.execute('SELECT COUNT(*) FROM restrictions').fetchone()[0]}")
changes = db.execute("SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL AND previous_value != limit_value").fetchone()[0]
print(f"Changes tracked: {changes}")
db.close()
