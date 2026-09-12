#!/usr/bin/env python3
"""Insert fresh restrictions found on July 16, 2026 from web searches."""
import sqlite3

db = sqlite3.connect('/root/diesel_limits/restrictions.db')

new = [
    # From lenta.ru (July 14 article - updated data)
    ("Республика Адыгея", None, "все АЗС", "физлица", "объем", "20-30л бензина, 60л дизеля, только в бак", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-14"),
    ("Республика Алтай", None, "все АЗС", "физлица", "запрет", "только раз в сутки при предъявлении СТС", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-14"),
    ("Архангельская область", "трасса М8", "все АЗС", "физлица", "объем", "полный бак для дальних поездок", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-14"),
    ("Республика Башкортостан", None, "все АЗС", "бюджетные организации", "объем", "исключение из лимитов для бюджетных организаций", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-14"),
    ("Белгородская область", None, "частные АЗС", "физлица", "запрет", "приостановлена продажа АИ-95 на отдельных АЗС", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-14"),
    ("Владимирская область", None, "все АЗС", "физлица", "режим", "режим экономии для служебного транспорта с 18 июня", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-14"),
    ("Забайкальский край", "Чита", "все АЗС", "физлица", "объем", "заправка по QR-кодам с 4 июля", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-14"),
    ("Иркутская область", "Нижнеилимский округ", "все АЗС", "физлица", "объем", "30л бензина, только 2 дня в неделю", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-14"),
    ("Краснодарский край", "Сочи", "все АЗС", "физлица", "объем", "30л бензина, 60л дизеля", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-14"),
    ("Курская область", None, "все АЗС", "физлица", "время", "заправка по четным/нечетным номерам с 15 июля", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-14"),
    ("Липецкая область", None, "все АЗС", "физлица", "объем", "30л бензина, дизель без ограничений", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-14"),
    ("Новосибирская область", None, "все АЗС", "физлица", "объем", "в канистры не более 10л", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-14"),
    ("Омская область", None, "все АЗС", "физлица", "объем", "с 6 июля разрешены канистры", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-14"),
    ("Приморский край", None, "АЗС ННК", "юрлица/грузовики", "объем", "до 100л в городе, до 200л на трассе для большегрузов", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-14"),
    ("Севастополь", None, "сеть АТАН", "физлица", "объем", "свободная продажа на 11 АЗС сети АТАН с 6 июля", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-14"),
    ("Республика Татарстан", None, "Татнефть", "физлица", "объем", "АИ-95 30л, дизель 60л; по топливным картам без ограничений", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-14"),
    ("Чувашская Республика", None, "Лукойл", "физлица", "объем", "до 20л бензина на авто", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-14"),
    ("Ямало-Ненецкий автономный округ", None, "частные АЗС", "физлица", "объем", "40-70л на машину", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "2026-07-14"),

    # From aa.com.tr
    ("Ставропольский край", None, "все АЗС", "физлица", "объем", "35л бензина на легковой автомобиль", "https://www.aa.com.tr/ru/%D0%BC%D0%B8%D1%80/%D0%B2-%D0%BD%D0%B5%D0%BA%D0%BE%D1%82%D0%BE%D1%80%D1%8B%D1%85-%D1%80%D0%B5%D0%B3%D0%B8%D0%BE%D0%BD%D0%B0%D1%85-%D1%80%D0%BE%D1%81%D1%81%D0%B8%D0%B8-%D0%B2%D0%B2%D0%BE%D0%B4%D1%8F%D1%82%D1%81%D1%8F-%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D1%8B%D0%B5-%D0%BB%D0%B8%D0%BC%D0%B8%D1%82%D1%8B-%D0%BD%D0%B0-%D0%BE%D1%82%D0%BF%D1%83%D1%81%D0%BA-%D0%B1%D0%B5%D0%BD%D0%B7%D0%B8%D0%BD%D0%B0/3974935", "2026-06-22"),
    ("Краснодарский край", None, "все АЗС", "физлица", "объем", "до 10л в канистры", "https://www.aa.com.tr/ru/%D0%BC%D0%B8%D1%80/%D0%B2-%D0%BD%D0%B5%D0%BA%D0%BE%D1%82%D0%BE%D1%80%D1%8B%D1%85-%D1%80%D0%B5%D0%B3%D0%B8%D0%BE%D0%BD%D0%B0%D1%85-%D1%80%D0%BE%D1%81%D1%81%D0%B8%D0%B8-%D0%B2%D0%B2%D0%BE%D0%B4%D1%8F%D1%82%D1%81%D1%8F-%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D1%8B%D0%B5-%D0%BB%D0%B8%D0%BC%D0%B8%D1%82%D1%8B-%D0%BD%D0%B0-%D0%BE%D1%82%D0%BF%D1%83%D1%81%D0%BA-%D0%B1%D0%B5%D0%BD%D0%B7%D0%B8%D0%BD%D0%B0/3974935", "2026-06-22"),

    # From sravni.ru table (July 15)
    ("Республика Мордовия", None, "все АЗС", "физлица", "объем", "20л бензина, 60л дизеля (легк); 300л дизеля (груз)", "https://www.sravni.ru/novost/2026/7/13/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-15"),
    ("Орловская область", None, "Роснефть, Газпром", "физлица", "время", "заправка по первой цифре госномера по дням недели", "https://www.sravni.ru/novost/2026/7/13/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-15"),
    ("Псковская область", None, "Сургутнефтегаз", "физлица", "время", "АИ-92 с 14:00 до полуночи; АИ-95 круглосуточно", "https://www.sravni.ru/novost/2026/7/13/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-15"),

    # Federal restrictions  
    ("Россия (федеральный уровень)", None, "правительство РФ", "все", "запрет", "запрет экспорта дизтоплива для производителей до 31 июля 2026", "https://rg.ru/2026/07/08/pravitelstvo-zapretilo-eksport-dizelnogo-topliva-ego-proizvoditeliam.html", "2026-07-08"),
]

inserted = 0
updated = 0
for r in new:
    region, city, network, client_type, limit_type, limit_value, src_url, src_date = r

    try:
        db.execute(
            """INSERT INTO restrictions(region,city,network,client_type,limit_type,limit_value,source_url,source_date,is_current,created_at,updated_at)
               VALUES(?,?,?,?,?,?,?,?,1,datetime('now'),datetime('now'))""",
            (region, city, network, client_type, limit_type, limit_value, src_url, src_date)
        )
        inserted += 1
    except sqlite3.IntegrityError:
        # Already exists — update value and flag as current
        db.execute(
            """UPDATE restrictions SET limit_value=?, source_url=?, source_date=?, is_current=1, updated_at=datetime('now')
               WHERE region=? AND network=? AND client_type=? AND limit_type=?""",
            (limit_value, src_url, src_date, region, network, client_type, limit_type)
        )
        updated += 1

db.commit()

# Re-normalize is_current
import subprocess, sys
subprocess.run([sys.executable, "/root/diesel_limits/normalize_current.py"], check=True)

total = db.execute('SELECT COUNT(*) FROM restrictions').fetchone()[0]
active = db.execute('SELECT COUNT(*) FROM restrictions WHERE is_current=1').fetchone()[0]
changes = db.execute('SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL').fetchone()[0]
db.close()

print(f"New restrictions inserted: {inserted}")
print(f"Existing restrictions updated: {updated}")
print(f"Total restrictions: {total}")
print(f"Active restrictions: {active}")
print(f"Changes tracked: {changes}")
