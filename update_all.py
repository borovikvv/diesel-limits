#!/usr/bin/env python3
"""Обновление: цены PetrolPlus → БД → карта → дамп. Ponytail: one shot."""
import sqlite3, json, os, sys
from datetime import datetime

ROOT = "/root/diesel_limits"
DB = f"{ROOT}/restrictions.db"
SRC = "https://www.petrolplus.ru/fuelindex/"
DATE = "04.07.2026"
NOW = datetime.now().strftime("%Y-%m-%d %H:%M")

# ── PetrolPlus diesel prices 04.07.2026 ──
prices = {
    "Москва": 79.28, "Санкт-Петербург": 79.79,
    "Алтайский край": 80.55, "Амурская область": 88.09,
    "Архангельская область": 82.59, "Астраханская область": 76.6,
    "Белгородская область": 76.53, "Брянская область": 75.25,
    "Владимирская область": 77.48, "Волгоградская область": 76.73,
    "Вологодская область": 83.18, "Воронежская область": 76.35,
    "Еврейская АО": 88.51, "Забайкальский край": 96.67,
    "Ивановская область": 76.12, "Иркутская область": 93.0,
    "Калининградская область": 81.33, "Калужская область": 76.06,
    "Камчатский край": 95.12, "Кемеровская область": 79.97,
    "Кировская область": 86.0, "Костромская область": 78.64,
    "Краснодарский край": 76.55, "Красноярский край": 89.43,
    "Курганская область": 79.9, "Курская область": 76.4,
    "Ленинградская область": 79.64, "Липецкая область": 75.5,
    "Московская область": 78.3, "Мурманская область": 87.0,
    "Нижегородская область": 77.15, "Новгородская область": 79.42,
    "Новосибирская область": 84.94, "Омская область": 78.87,
    "Оренбургская область": 79.2, "Орловская область": 75.0,
    "Пензенская область": 77.65, "Пермский край": 81.17,
    "Приморский край": 88.14, "Псковская область": 80.1,
    "Республика Адыгея": 76.5, "Республика Алтай": 88.48,
    "Республика Башкортостан": 77.5, "Республика Бурятия": 85.05,
    "Республика Дагестан": 98.26, "Республика Ингушетия": 75.9,
    "Республика Калмыкия": 75.95, "Республика Карелия": 83.32,
    "Республика Коми": 80.09, "Республика Марий Эл": 76.05,
    "Республика Мордовия": 78.05, "Республика Саха (Якутия)": 97.0,
    "Республика Северная Осетия — Алания": 73.9,
    "Республика Татарстан": 76.12, "Республика Тыва": 96.5,
    "Республика Хакасия": 83.5, "Ростовская область": 76.7,
    "Рязанская область": 76.2, "Самарская область": 76.25,
    "Сахалинская область": 94.33, "Саратовская область": 77.5,
    "Свердловская область": 79.85, "Смоленская область": 76.75,
    "Ставропольский край": 76.85, "Тамбовская область": 75.27,
    "Тверская область": 78.85, "Томская область": 82.7,
    "Тульская область": 76.65, "Тюменская область": 80.67,
    "Удмуртская Республика": 79.05, "Ульяновская область": 76.6,
    "Хабаровский край": 87.14, "Ханты-Мансийский АО — Югра": 86.24,
    "Челябинская область": 78.95, "Чеченская Республика": 83.33,
    "Чувашская Республика": 76.05, "Ямало-Ненецкий АО": 84.73,
    "Ярославская область": 77.51,
    "Кабардино-Балкарская Республика": 75.7,
    "Карачаево-Черкесская Республика": 74.5,
    "Ненецкий АО": 0, "Магаданская область": 99.0,
    "Чукотский АО": 85.0,
    "Республика Крым": 127.45, "Севастополь": 101.63,
}

# ── Ограничения: данные Lenta.ru (03.07.2026) + Sravni (03.07.2026) ──
restrictions = [
    # (регион, город, сеть, клиент, тип, значение, url, дата)
    ("Республика Крым", None, None, "все", "запрет", "АИ-92 до 20 л, АИ-95 для экстренных, дизель не указан",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Севастополь", None, None, "все", "запрет", "свободная продажа только на 8 АЗС, до конца июля",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Республика Дагестан", None, None, "физлица", "объем", "до 20 л бензин, до 50 л дизель",
     "https://tass.ru/obschestvo/27855585", "25.06.2026"),
    ("Краснодарский край", "Краснодар", None, "физлица", "объем", "20-30 л бензин; 30-60 л дизель; только в бак",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Краснодарский край", "Сочи", None, "физлица", "объем", "до 30 л бензин, до 60 л дизель",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Москва", None, "Газпромнефть", "физлица", "объем", "до 30 л бензин, до 60 л дизель (200 на трассе)",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Москва", None, "Лукойл", "физлица", "объем", "до 20-30 л бензин",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Москва", None, "Teboil", "физлица", "объем", "до 20-30 л бензин, до 60 л дизель",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Санкт-Петербург", None, None, "физлица", "объем", "20-30 л бензин, до 60 л дизель (зависит от сети)",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Московская область", None, None, "физлица", "объем", "20-30 л бензин, 60 л дизель (200 на трассе)",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Ленинградская область", None, None, "физлица", "объем", "20-30 л на авто, запрет канистр",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Республика Татарстан", None, "Татнефть", "физлица", "объем", "30 л АИ-95; дизель без ограничений по топливным картам",
     "https://tass.ru/obschestvo/27749331", "03.07.2026"),
    ("Иркутская область", None, None, "физлица", "объем", "до 50 л приоритет экстренным; Нижнеилимский — 30 л 2 дня/нед",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Забайкальский край", "Чита", None, "физлица", "объем", "до 15 л бензин, только в бак; с 4.07 QR-коды",
     "https://tass.ru/obschestvo/27856445", "03.07.2026"),
    ("Мурманская область", None, "Лукойл", "физлица", "объем", "30 л бензин, до 60 л дизель",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Мурманская область", None, "Роснефть", "физлица", "объем", "до 99 л бензин",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Мурманская область", None, "Газпромнефть", "физлица", "объем", "30 л бензин и дизель; по картам — 60 л дизель",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Кемеровская область", None, "Газпромнефть", "физлица", "объем", "40 л бензин, 80 л дизель (200 на трассе)",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Омская область", None, None, "физлица", "объем", "40 л бензин, 80 л дизель; на трассах 200 л дизель",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Вологодская область", None, "Лукойл", "физлица", "объем", "30 л бензин, 60 л дизель (200 на трассе)",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Воронежская область", None, "Лукойл", "физлица", "объем", "30 л бензин, 60 л дизель (200 на трассе)",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Калининградская область", None, None, "физлица", "объем", "30 л бензин, 60 л дизель, только в бак",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Курганская область", None, None, "физлица", "объем", "40 л бензин, 80 л дизель (200 на трассе); канистры до 10 л",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Тюменская область", None, "Газпромнефть", "физлица", "объем", "40 л бензин, 80 л дизель (200 на трассе); только в бак",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Ульяновская область", None, None, "физлица", "объем", "40 л бензин, 100 л дизель; грузовики — 300 л дизель",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Саратовская область", None, None, "физлица", "объем", "30 л бензин; до 15.07.2026",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Орловская область", None, None, "физлица", "объем", "30-50 л бензин; с 4.07 по номерам авто",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Ямало-Ненецкий АО", None, None, "физлица", "запрет", "запрет канистр; 40-70 л на авто",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Белгородская область", None, "Лукойл", "физлица", "объем", "30 л бензин, 60 л дизель",
     "https://tass.ru/ekonomika/27849387", "03.07.2026"),
    ("Липецкая область", None, None, "физлица", "объем", "30 л бензин, только в бак; дизель без ограничений; до 5.07",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Приморский край", None, None, "все", "объем", "100 л дизель в городе, 200 на трассе (для большегрузов); только в бак",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Пензенская область", None, None, "физлица", "объем", "100 л бензин, 200 л дизель; только в бак",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Республика Саха (Якутия)", None, "Саханефтегазсбыт", "физлица", "объем", "30 л бензин, 200 л дизель",
     "https://www.gazeta.ru/social/news/2026/06/29/28785277.shtml", "03.07.2026"),
    ("Республика Башкортостан", None, None, "физлица", "объем", "30 л бензин на авто",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Республика Адыгея", None, None, "физлица", "объем", "легковые — 20-30 л; дизель 60 л",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Волгоградская область", None, "Лукойл", "физлица", "объем", "30 л бензин, 60 л дизель (200 на трассе)",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Свердловская область", None, "Газпромнефть", "физлица", "объем", "40 л бензин и дизель",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Новосибирская область", None, "Газпромнефть", "физлица", "объем", "40 л бензин, 80 л дизель (200 на трассе); канистры 10 л",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Республика Мордовия", None, None, "физлица", "объем", "30 л бензин, 60 л дизель (грузовые — 300 л)",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Псковская область", None, "Татнефть", "физлица", "объем", "20 л бензин АИ-95, 40 л дизель",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Самарская область", None, None, "физлица", "объем", "40 л бензин, 100 л дизель; с 24.06 на 2 нед",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Ханты-Мансийский АО — Югра", None, None, "физлица", "объем", "40 л бензин, 80 л дизель с конца июня",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Республика Алтай", "Горно-Алтайск", None, "физлица", "объем", "30 л бензин, 50 л дизель; остальные — 50/100 л; до 1.09",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Ивановская область", None, None, "физлица", "объем", "30 л бензин, 60 л дизель, запрет канистр",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "02.07.2026"),
    ("Архангельская область", None, None, "физлица", "объем", "20-50 л; на М8 — полный бак",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "02.07.2026"),
    ("Карелия", None, None, "физлица", "объем", "20-60 л, запрет канистр",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Брянская область", None, None, "физлица", "запрет", "запрет продажи в канистры; до 20 л на авто",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Владимирская область", None, None, "физлица", "объем", "20-30 л бензин, до 40 л дизель; режим экономии",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Курская область", None, None, "физлица", "запрет", "запрет канистр; 20-30 л в бак; в приграничье можно в канистры",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Чувашская Республика", None, "Татнефть", "физлица", "объем", "30 л АИ-95; АИ-92 и дизель без ограничений",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Тамбовская область", None, None, "физлица", "объем", "30 л, запрет канистр",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Тверская область", None, None, "физлица", "объем", "зависит от АЗС; спецтранспорт 5:30-7:30",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Красноярский край", None, None, "физлица", "объем", "до 40 л бензин, запрет канистр",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Смоленская область", None, None, "физлица", "объем", "30 л бензин, 60 л дизель; запрет канистр",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Кировская область", None, None, "физлица", "объем", "30-100 л бензин, до 100 л дизель",
     "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm", "03.07.2026"),
    ("Новгородская область", None, "Сургутнефтегаз", "все", "время", "5:00-8:00 только экстренные службы",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
    ("Челябинская область", "Кыштым", None, "население", "объем", "ограничена продажа бензина",
     "https://www.sravni.ru/novost/2026/7/1/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "03.07.2026"),
]

# ── 1. Prices ──
db = sqlite3.connect(DB)
c = db.cursor()
pc, cc = 0, 0
for r, p in prices.items():
    if p > 0:
        c.execute("INSERT OR REPLACE INTO prices(region,price,source_url,source_date,updated_at) VALUES(?,?,?,?,datetime('now'))",
                  (r, p, SRC, DATE))
        pc += 1
print(f"Prices: {pc} regions")

# ── 2. Restrictions ──
for reg, city, net, ct, lt, val, url, date in restrictions:
    net_clean = net if net else ""
    cur = c.execute("SELECT id, limit_value FROM restrictions WHERE region=? AND COALESCE(network,'')=COALESCE(?,'') AND client_type=? AND limit_type=? AND is_current=1",
                    (reg, net_clean, ct, lt)).fetchone()
    if cur and cur[1] != val:
        c.execute("UPDATE restrictions SET is_current=0, previous_value=limit_value, updated_at=datetime('now') WHERE id=?", (cur[0],))
        cc += 1
    if not cur or cur[1] != val:
        c.execute("INSERT OR IGNORE INTO restrictions(region,city,network,client_type,limit_type,limit_value,source_url,source_date) VALUES(?,?,?,?,?,?,?,?)",
                  (reg, city, net, ct, lt, val, url, date))
db.commit()

total = c.execute("SELECT COUNT(*) FROM restrictions WHERE is_current=1").fetchone()[0]
all_t = c.execute("SELECT COUNT(*) FROM restrictions").fetchone()[0]
print(f"Restrictions: {len(restrictions)} new/updated, {cc} changed, {total} active, {all_t} total")
db.close()
print("Done. DB updated.")
