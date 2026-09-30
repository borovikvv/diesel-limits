"""Insert fresh diesel restrictions — Sept 2026 update based on web search results"""
import sqlite3
from datetime import datetime

DB = "/root/diesel_limits/restrictions.db"
conn = sqlite3.connect(DB)
c = conn.cursor()

TODAY = "2026-09-28"

# (region, city, station_network, client_type, limit_type, value, url, source_date, notes)
RESTRICTIONS = [
    # Key active restrictions as of late Sept 2026
    ("Республика Саха (Якутия)", None, "разные АЗС", "все", "объем", "50-200 л дизеля", "https://www.sravni.ru/novost/2026/8/26/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", TODAY, "по топливным картам или только в бак"),
    ("Забайкальский край", None, "разные АЗС", "все", "объем", "до 50 л", "https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/", TODAY, "10-50 л на авто"),
    ("Республика Дагестан", None, "все АЗС", "физлица", "объем", "50 л дизеля", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", TODAY, "только в бак, 20л бенз+50л диз"),
    ("Красноярский край", None, "разные АЗС", "все", "объем", "до 100 л дизеля город, 200 трасса", "https://lenta.ru/news/2026/06/17/rossiyskaya-neftyanaya-kompaniya-snyala-ogranicheniya-na-prodazhu-topliva/", TODAY, "некоторые АЗС отменяют лимиты с 13 августа"),
    ("Иркутская область", None, "все АЗС", "физлица", "объем", "80 л дизеля", "https://news.mail.ru/economics/71391449/", TODAY, "только в бак"),
    ("Приморский край", None, "все АЗС", "грузовики", "объем", "100 л город, 200 трасса", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", TODAY, "для большегрузов"),
    ("Республика Бурятия", None, "все АЗС", "все", "объем", "100 л дизеля", "https://news.mail.ru/economics/71391449/", TODAY, "40 л бенз, 100 л дизель"),
    ("Хабаровский край", None, "разные АЗС", "все", "объем", "до 100 л дизеля", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", TODAY, "некоторые АЗС снимают с 25 августа"),
    ("Амурская область", None, "все АЗС", "все", "объем", "до 100 л дизеля", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", TODAY, "только в бак"),
    ("Мурманская область", None, "все АЗС", "все", "объем", "60 л дизеля", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", TODAY, "в городе"),
    ("Республика Коми", None, "все АЗС", "все", "объем", "60 л дизеля", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", TODAY, "в городе"),
    ("Архангельская область", None, "все АЗС", "все", "объем", "60 л дизеля", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", TODAY, "только в бак"),
    ("Вологодская область", None, "все АЗС", "все", "объем", "60 л город, 200 трасса", "https://finance.mail.ru/article/problemy-s-benzinom-v-rf-gde-dejstvuyut-ogranicheniya-i-kogda-normalizuetsya-situaciya-69215089/", TODAY, "30 л бенз, 60/200 диз"),
    ("Калининградская область", None, "Лукойл, Сургутнефтегаз", "все", "отмена", "без ограничений", "https://www.sravni.ru/novost/2026/8/26/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", TODAY, "с 28 июля отменены"),
    ("Псковская область", None, "сетевые АЗС", "все", "объем", "40 л дизеля", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", TODAY, "30+ л на сетевых"),
    ("Удмуртия", None, "разные АЗС", "все", "объем", "80-400 л дизеля", "https://www.sravni.ru/novost/2026/8/26/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", TODAY, "зависит от АЗС"),
    ("Томская область", None, "разные АЗС", "все", "объем", "80 л дизеля", "https://www.sravni.ru/novost/2026/8/26/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", TODAY, "30-40 бенз, 80 диз"),
    ("Республика Хакасия", None, "все АЗС", "все", "объем", "до 80 л дизеля", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", TODAY, ""),
    ("Новосибирская область", None, "все АЗС", "все", "объем", "60 л дизеля", "https://www.sravni.ru/novost/2026/8/26/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", TODAY, "30 бенз, 60 дизель, запрещена продажа до 18 лет"),
    ("Кемеровская область", None, "все АЗС", "физлица", "объем", "80 л дизеля город, 200 трасса", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", TODAY, "до 40 л бензина"),
    ("Алтайский край", None, "все АЗС", "все", "объем", "100 л дизеля", "https://www.sravni.ru/novost/2026/8/26/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", TODAY, "50 л бенз, 100 л диз, до 1 сентября"),
    ("Омская область", None, "все АЗС", "все", "объем", "60 л дизеля", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", TODAY, ""),
    ("Тюменская область", "Газпромнефть", "Газпромнефть", "все", "объем", "80 л город, 200 трасса", "https://www.sravni.ru/novost/2026/8/26/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", TODAY, "только в бак"),
    ("Курганская область", None, "все АЗС", "все", "объем", "80 л город, 200 трасса", "https://www.sravni.ru/novost/2026/8/26/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", TODAY, "только в бак"),
    ("Ямало-Ненецкий АО", None, "сетевые АЗС", "все", "запрет", "запрет в тару", "https://news.mail.ru/economics/71391449/", TODAY, "40-70 л лимит на частных"),
    ("Ханты-Мансийский АО", None, "все АЗС", "все", "объем", "до 100 л дизеля", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", TODAY, ""),
    ("Свердловская область", None, "разные АЗС", "все", "объем", "60 л город, 200 трасса", "https://www.sravni.ru/novost/2026/8/26/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", TODAY, "30-40 л в Екатеринбурге"),
    ("Челябинская область", None, "разные АЗС", "все", "объем", "60 л дизеля", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", TODAY, "20-30 л бензина"),
    ("Пермский край", None, "все АЗС", "все", "объем", "до 100 л дизеля", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", TODAY, ""),
    ("Республика Татарстан", None, "Татнефть", "все", "объем", "60 л дизеля", "https://www.rbc.ru/economics/19/08/2026/6a84bb959a7947c0ad9b886f", TODAY, "на АЗС Татнефти лимит 60л диз"),
    ("Москва", None, "разные АЗС", "все", "объем", "до 60 л дизеля", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", TODAY, "20-30 л бензин, 60 дизель, до 200 трасса"),
    ("Санкт-Петербург", None, "все АЗС", "все", "объем", "60 л дизеля", "https://www.rbc.ru/economics/24/06/2026/6a3c13c59a7947597979e6a3", TODAY, "30 л бензин АИ-92/95"),
    ("Ростовская область", None, "все АЗС", "все", "объем", "60 л легковые, 200 грузовые", "https://rostov.rbc.ru/rostov/freenews/6a50eb5d9a794716bc468efe", TODAY, "лимит на отпуск"),
    ("Краснодарский край", None, "разные АЗС", "все", "объем", "60 л дизеля", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", TODAY, "20-30 л бензина"),
    ("Крым и Севастополь", None, "все АЗС", "все", "объем", "40 л дизеля", "https://www.sravni.ru/novost/2026/8/26/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", TODAY, "20 л бенз по QR-кодам, диз свободнее"),
    ("Липецкая область", None, "все АЗС", "все", "отмена", "без ограничений дизеля", "https://www.sravni.ru/novost/2026/8/26/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", TODAY, "дизель без ограничений"),
    ("Ивановская область", None, "все АЗС", "все", "объем", "60-200 л дизеля", "https://www.sravni.ru/novost/2026/8/26/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", TODAY, "30 л бензин, только в бак"),
    ("Владимирская область", None, "ряд АЗС", "все", "время", "7:00-10:00 только экстренные", "https://www.sravni.ru/novost/2026/8/26/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", TODAY, "утренний лимит по времени"),
    ("Калужская область", None, "все АЗС", "все", "чет-нечет", "чет/нечет по номерам", "https://www.sravni.ru/novost/2026/8/26/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", TODAY, "НЕ распространяется на дизель"),
    ("Тверская область", None, "ряд АЗС", "все", "время", "5:30-7:30 только экстренные", "https://www.sravni.ru/novost/2026/8/26/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", TODAY, ""),
    ("Нижегородская область", None, "все АЗС", "все", "чет-нечет", "чет/нечет по номерам", "https://www.sravni.ru/novost/2026/8/26/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/", TODAY, "30-60 л бензин"),
]

inserted = 0
for r in RESTRICTIONS:
    region, city, network, client, ltype, value, url, sdate, notes = r
    try:
        c.execute("""
            INSERT INTO restrictions(
                region, city, network, client_type, limit_type,
                limit_value, source_url, source_date, is_current, previous_value, created_at, updated_at
            ) VALUES (?,?,?,?,?,?,?,?,1,NULL,datetime('now'),datetime('now'))
        """, (region, city, network, client, ltype, value, url, sdate))
        inserted += 1
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        print(f"Skip {region}: {e}")

conn.commit()
print(f"Inserted {inserted} restrictions")
print(f"Active: {c.execute('SELECT COUNT(*) FROM restrictions WHERE is_current=1').fetchone()[0]}")
print(f"Total: {c.execute('SELECT COUNT(*) FROM restrictions').fetchone()[0]}")
conn.close()
