#!/usr/bin/env python3
"""Insert all collected diesel restrictions into the database."""
import sqlite3
from datetime import datetime

DB = "/root/diesel_limits/restrictions.db"
TODAY = "2026-07-27"

# (region, network, client_type, limit_type, limit_value, source_url, source_date)
restrictions = [
    # Крым и Севастополь — самые жёсткие
    ("Республика Крым", "все сети", "физлица", "запрет",
     "Полный запрет продажи для физлиц. Только госслужбы, экстренные службы, общественный транспорт",
     "https://www.vedomosti.ru/business/articles/2026/06/21/1207557-krimu-prekratili-prodazhu", "2026-06-21"),
    ("Республика Крым", "все сети", "юридические лица", "запрет",
     "Полный запрет продажи для юрлиц. Только госслужбы",
     "https://www.vedomosti.ru/business/articles/2026/06/21/1207557-krimu-prekratili-prodazhu", "2026-06-21"),
    ("Севастополь", "все сети", "физлица", "запрет",
     "Полный запрет. С 4 июля 9 АЗС начали продажу дизеля Ultra в свободной продаже",
     "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-06-21"),

    # Дагестан
    ("Республика Дагестан", "все сети", "физлица", "объем",
     "Не более 50 л дизеля в одни руки",
     "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-06-25"),

    # Владимирская область
    ("Владимирская область", "все сети", "физлица", "объем",
     "40 л дизеля за одну заправку. Запрет продажи в канистры",
     "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-06-18"),

    # Омская область
    ("Омская область", "все сети", "физлица", "объем",
     "80 л дизеля в городе, 200 л на трассовых АЗС. Разрешена заправка в канистры с 6 июля",
     "https://www.vedomosti.ru/business/articles/2026/06/24/1208285-ob-ogranicheniyah-benzina", "2026-06-23"),
    ("Омская область", "все сети", "юридические лица", "объем",
     "Грузовики: 200 л на трассовых АЗС",
     "https://www.vedomosti.ru/business/articles/2026/06/24/1208285-ob-ogranicheniyah-benzina", "2026-06-23"),

    # Кемеровская область
    ("Кемеровская область", "Газпромнефть", "физлица", "объем",
     "80 л дизеля, на трассовых АЗС до 200 л",
     "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "2026-06-24"),

    # Татарстан
    ("Республика Татарстан", "Татнефть", "физлица", "объем",
     "60 л дизеля для легковых, 300 л для грузовиков. По топливным картам лимита нет. Только в бак",
     "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-06-13"),
    ("Республика Татарстан", "Газпромнефть", "физлица", "объем",
     "60 л дизеля в одни руки",
     "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "2026-06-15"),
    ("Республика Татарстан", "Татнефть", "юридические лица", "объем",
     "300 л дизеля для грузовиков",
     "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-06-13"),

    # Приморский край
    ("Приморский край", "все сети", "юридические лица", "объем",
     "Большегрузы: до 100 л в городе, до 200 л на трассе",
     "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-06-29"),

    # Воронежская область
    ("Воронежская область", "Лукойл", "физлица", "объем",
     "60 л дизеля в городе, 200 л на трассе. Запрет продажи в канистры",
     "https://www.vedomosti.ru/business/articles/2026/06/24/1208285-ob-ogranicheniyah-benzina", "2026-06-23"),

    # Пензенская область
    ("Пензенская область", "все сети", "физлица", "объем",
     "200 л дизеля на машину. Только в бак",
     "https://www.vedomosti.ru/business/articles/2026/06/24/1208285-ob-ogranicheniyah-benzina", "2026-06-23"),

    # Мурманская область
    ("Мурманская область", "Лукойл", "физлица", "объем",
     "60 л дизельного топлива",
     "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "2026-06-24"),
    ("Мурманская область", "Роснефть", "физлица", "объем",
     "Дизель без ограничений",
     "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "2026-06-24"),
    ("Мурманская область", "Газпромнефть", "физлица", "объем",
     "30 л дизеля, по карте лояльности 60 л. Запрет канистр",
     "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "2026-06-24"),

    # Самарская область
    ("Самарская область", "все сети", "физлица", "объем",
     "100 л дизеля для легковых. Запрет продажи в канистры. Только в бак",
     "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "2026-06-25"),
    ("Самарская область", "все сети", "юридические лица", "объем",
     "300 л дизеля для грузовиков",
     "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-06-25"),

    # Ростовская область
    ("Ростовская область", "все сети", "физлица", "объем",
     "60 л дизеля для легковых, 200 л для грузовиков, 300 л для пассажирского транспорта. Без ограничений экстренные службы",
     "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "2026-06-24"),

    # Калининградская область
    ("Калининградская область", "все сети", "физлица", "объем",
     "60 л дизеля в один бак",
     "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "2026-06-24"),

    # Вологодская область
    ("Вологодская область", "Лукойл", "физлица", "объем",
     "60 л дизеля в городе, 200 л на трассовых АЗС",
     "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "2026-06-23"),

    # Белгородская область
    ("Белгородская область", "Лукойл", "физлица", "объем",
     "60 л дизельного топлива",
     "https://www.vedomosti.ru/business/articles/2026/06/24/1208285-ob-ogranicheniyah-benzina", "2026-06-23"),
    ("Белгородская область", "Роснефть", "физлица", "объем",
     "Запрещена заправка в канистры",
     "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "2026-06-23"),

    # Москва
    ("Москва", "Газпромнефть", "физлица", "объем",
     "60 л дизеля в городе, 200 л на трассовых АЗС. Только в бак",
     "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-06-22"),
    ("Москва", "Лукойл", "физлица", "объем",
     "20–30 л бензина. Дизель — без ограничений на некоторых АЗС",
     "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "2026-06-22"),

    # Московская область
    ("Московская область", "Teboil", "физлица", "объем",
     "60 л дизеля, 20–30 л бензина",
     "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-06-22"),

    # Якутия
    ("Республика Саха (Якутия)", "Саханефтегазсбыт", "физлица", "объем",
     "200 л дизеля на машину. Запрет продажи в переносную тару",
     "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "2026-06-24"),

    # Ульяновская область
    ("Ульяновская область", "все сети", "физлица", "объем",
     "100 л дизеля на легковой автомобиль",
     "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "2026-06-24"),
    ("Ульяновская область", "все сети", "юридические лица", "объем",
     "300 л дизеля для грузовиков и автобусов",
     "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "2026-06-24"),

    # Республика Алтай
    ("Республика Алтай", "все сети", "физлица", "объем",
     "50–100 л дизеля в сутки в зависимости от района. Продажа по СТС. Электронная система контроля",
     "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "2026-07-09"),

    # Томская область
    ("Томская область", "все сети", "физлица", "объем",
     "80 л дизеля на некоторых АЗС",
     "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-06-24"),

    # Адыгея
    ("Республика Адыгея", "все сети", "физлица", "объем",
     "Ограничения на объем, лимиты не сообщаются. Призыв воздержаться от поездок",
     "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-06-24"),

    # Краснодарский край
    ("Краснодарский край", "все сети", "физлица", "объем",
     "30–60 л дизеля. Запрет продажи в канистры",
     "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-01"),

    # Псковская область
    ("Псковская область", "все сети", "физлица", "объем",
     "40 л дизеля",
     "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-06-15"),

    # Удмуртия
    ("Удмуртская Республика", "Татнефть", "физлица", "объем",
     "40 л дизеля (изначально), затем лимит снят",
     "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-06-12"),
    ("Удмуртская Республика", "Татнефть", "юридические лица", "объем",
     "200 л дизеля для грузовиков",
     "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-06-12"),

    # Мордовия
    ("Республика Мордовия", "все сети", "физлица", "объем",
     "60 л дизеля на легковой автомобиль. По номерам (чет/нечет)",
     "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-01"),
    ("Республика Мордовия", "все сети", "юридические лица", "объем",
     "300 л дизеля для грузовиков",
     "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-01"),

    # Карелия
    ("Республика Карелия", "все сети", "физлица", "объем",
     "60 л дизеля. Минимальный объём отпуска — 10 л. Только в бак",
     "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-01"),
    ("Республика Карелия", "все сети", "юридические лица", "объем",
     "250 л дизеля для большегрузов и спецтехники",
     "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-01"),

    # Курганская область
    ("Курганская область", "все сети", "физлица", "объем",
     "80 л дизеля в населённых пунктах, 200 л на трассах. Только в бак",
     "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-01"),

    # Свердловская область
    ("Свердловская область", "Газпромнефть", "физлица", "объем",
     "40 л дизеля",
     "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-01"),

    # Ивановская область
    ("Ивановская область", "все сети", "физлица", "объем",
     "60–200 л дизеля в зависимости от АЗС. Только в бак",
     "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-06-24"),

    # ЯНАО
    ("Ямало-Ненецкий АО", "сетевые АЗС", "физлица", "запрет",
     "Запрет на отпуск топлива в тару. На частных АЗС — лимит 40–70 л на машину",
     "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-06-24"),

    # Чувашия
    ("Чувашская Республика", "все сети", "физлица", "объем",
     "30 л бензина в день",
     "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-01"),
    ("Чувашская Республика", "все сети", "юридические лица", "объем",
     "300 л дизеля для грузовиков и коммунальной техники",
     "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-01"),

    # Волгоградская область
    ("Волгоградская область", "Лукойл", "физлица", "объем",
     "60 л дизтоплива в городе, 200 л на трассе",
     "https://www.vedomosti.ru/business/articles/2026/06/24/1208285-ob-ogranicheniyah-benzina", "2026-06-23"),

    # Тамбовская область
    ("Тамбовская область", "все сети", "физлица", "запрет",
     "Запрет на отпуск дизеля в канистры и другую тару",
     "https://www.vedomosti.ru/business/articles/2026/06/24/1208285-ob-ogranicheniyah-benzina", "2026-06-23"),

    # Забайкальский край
    ("Забайкальский край", "все сети", "физлица", "объем",
     "15 л топлива. Режим повышенной готовности. Только в баки. Неснижаемый резерв для экстренных служб",
     "https://zona.media/article/2026/06/26/fuel-limit", "2026-06-25"),

    # Брянская область
    ("Брянская область", "все сети", "физлица", "запрет",
     "Запрет на продажу топлива в канистры и другие ёмкости",
     "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "2026-06-23"),

    # Оренбургская область
    ("Оренбургская область", "Башнефть", "физлица", "объем",
     "30 л бензина и дизеля",
     "https://zona.media/article/2026/06/26/fuel-limit", "2026-06-20"),

    # Кировская область
    ("Кировская область", "Движение", "физлица", "объем",
     "100 л дизеля. По чётным/нечётным датам с 11 июля",
     "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "2026-07-11"),
    ("Кировская область", "Лукойл", "физлица", "объем",
     "100 л бензина",
     "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "2026-07-11"),

    # Нижегородская область
    ("Нижегородская область", "Движение", "физлица", "объем",
     "40 л бензина. По номерам (чет/нечет)",
     "https://www.sravni.ru/novost/2026/7/16/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-06-24"),

    # Астраханская область
    ("Астраханская область", "все сети", "физлица", "время",
     "Продажа по госномерам: чётные дни — чётный номер, нечётные — нечётный. С 9 июля",
     "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "2026-07-09"),

    # Липецкая область
    ("Липецкая область", "все сети", "физлица", "объем",
     "30 л бензина на автомобиль. Ограничения продлены",
     "https://www.kommersant.ru/doc/8778047", "2026-06-30"),

    # Магаданская область
    ("Магаданская область", "все сети", "физлица", "запрет",
     "Все виды топлива только в бак автомобиля",
     "https://zona.media/article/2026/06/26/fuel-limit", "2026-06-24"),

    # Саратовская область
    ("Саратовская область", "все сети", "физлица", "объем",
     "30 л бензина на машину (23–30 июня)",
     "https://www.vedomosti.ru/business/articles/2026/06/24/1208285-ob-ogranicheniyah-benzina", "2026-06-23"),

    # Новосибирская область
    ("Новосибирская область", "все сети", "физлица", "объем",
     "30 л бензина на машину (ограничения введены 23 июня)",
     "https://www.vedomosti.ru/business/articles/2026/06/24/1208285-ob-ogranicheniyah-benzina", "2026-06-23"),
]

# ── Insert restrictions ──
db = sqlite3.connect(DB)
inserted = 0
updated = 0

for r in restrictions:
    region, network, client_type, limit_type, limit_value, source_url, source_date = r
    # UPSERT: INSERT OR REPLACE with explicit id handling
    existing = db.execute(
        "SELECT id, limit_value FROM restrictions WHERE region=? AND network=? AND client_type=? AND limit_type=?",
        (region, network or "", client_type or "", limit_type)
    ).fetchone()
    if existing:
        if existing[1] != limit_value:
            db.execute(
                "UPDATE restrictions SET limit_value=?, previous_value=?, source_url=?, source_date=?, is_current=1, updated_at=datetime('now') WHERE id=?",
                (limit_value, existing[1], source_url, source_date, existing[0])
            )
            updated += 1
        else:
            db.execute(
                "UPDATE restrictions SET source_url=?, source_date=?, is_current=1, updated_at=datetime('now') WHERE id=?",
                (source_url, source_date, existing[0])
            )
    else:
        db.execute(
            "INSERT INTO restrictions(region,network,client_type,limit_type,limit_value,source_url,source_date,is_current,updated_at) "
            "VALUES(?,?,?,?,?,?,?,1,datetime('now'))",
            (region, network, client_type, limit_type, limit_value, source_url, source_date)
        )
        inserted += 1

db.commit()
db.close()
print(f"Restrictions: {inserted} new, {updated} updated")
