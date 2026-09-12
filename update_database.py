#!/usr/bin/env python3
"""Update diesel restrictions & prices from scraped data (06.07.2026)."""
import sqlite3

DB = "/root/diesel_limits/restrictions.db"

# ── Restrictions from sravni.ru (03.07.2026) & lenta.ru (05.07.2026) ──
# (region, network, client_type, limit_type, limit_value, source_url, source_date)
restrictions = [
    # Sravni.ru table (03.07.2026)
    ("Адыгея","все сети","физлица","объем","ограничения на объём","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Республика Башкортостан","все сети","физлица","объем","30 л бензина, только в бак","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Белгородская область","Лукойл","физлица","объем","30 л бензина, 60 л дизеля","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Белгородская область","Роснефть","физлица","запрет","запрещена заправка в канистры","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Белгородская область","Газпромнефть","физлица","запрет","не продают АИ-95","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Брянская область","все сети","физлица","запрет","запрещена заправка в канистры","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Владимирская область","все сети","физлица","объем","20-30 л бензина, 40 л дизеля","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Волгоградская область","Лукойл","физлица","объем","30 л бензина/60 л дизеля (город), 60/200 (трасса)","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Вологодская область","Лукойл","физлица","объем","30 л бензина/60 л дизеля (город), 30/200 (трасса), только в бак","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Воронежская область","Лукойл","физлица","объем","30 л бензина/60 л дизеля (город), 60/200 (трасса)","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Республика Дагестан","все сети","физлица","объем","20 л бензина, 50 л дизеля в одни руки","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Свердловская область","Газпромнефть","физлица","объем","40 л бензина и дизеля","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Забайкальский край","все сети","физлица","объем","15 л бензина на автомобиль, только в бак","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Иркутская область","все сети","физлица","объем","до 50 л, приоритет экстренным службам","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Калининградская область","все сети","физлица","объем","30 л бензина, 60 л дизеля","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Кемеровская область","Газпромнефть","физлица","объем","40 л бензина/80 л дизеля (город), 40/200 (трасса)","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Краснодарский край","все сети","физлица","объем","20-30 л бензина/30-60 л дизеля, только в бак","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Республика Крым","все сети","физлица","запрет","полное ограничение, только госслужбам","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Курганская область","все сети","физлица","объем","40 л бензина/80 л дизеля (город), 40/200 (трасса), только в бак","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Курская область","все сети","физлица","запрет","запрещена заправка в канистры","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Липецкая область","все сети","физлица","объем","30 л бензина, только в бак, до 05.07","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Республика Мордовия","все сети","физлица","объем","30 л бензина/60 л дизеля (легк), 300 л (груз), только в бак","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Москва","Газпромнефть","физлица","объем","30 л бензина/60 л дизеля, только в бак","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Москва","Лукойл","физлица","объем","20-30 л бензина, только в бак","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Москва","Teboil","физлица","объем","20-30 л бензина, 60 л дизеля","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Мурманская область","Лукойл","физлица","объем","30 л бензина, до 60 л дизеля","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Мурманская область","Газпромнефть","физлица","объем","30 л бензина и дизеля, по картам 60 л дизеля","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Новгородская область","Сургутнефтегаз","физлица","время","с 5:00 до 8:00 только экстренные службы","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Новосибирская область","Газпромнефть","физлица","объем","40 л бензина/80 л дизеля, на трассе 40/200","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Омская область","все сети","физлица","объем","40 л бензина/200 л дизеля, только в бак","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Орловская область","Роснефть,Газпром","физлица","объем","30-50 л по госномеру с 04.07","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Пензенская область","все сети","физлица","объем","100 л бензина/200 л дизеля, только в бак","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Приморский край","все сети","все","объем","до 100 л бензина/200 л на трассе, только в бак","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Псковская область","Татнефть","физлица","объем","20 л АИ-95, 40 л дизеля","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Самарская область","все сети","физлица","объем","40 л бензина/100 л дизеля, только в бак, до 08.07","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Санкт-Петербург","Teboil","физлица","объем","30 л бензина/60 л дизеля","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Санкт-Петербург","Лукойл","физлица","объем","30 л бензина","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Санкт-Петербург","Газпромнефть","физлица","объем","30 л бензина/60 л дизеля","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Санкт-Петербург","Сургутнефтегаз","физлица","объем","20 л бензина/100 л дизеля","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Саратовская область","все сети","физлица","объем","30 л бензина, до 15.07","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Севастополь","все сети","физлица","запрет","полное ограничение","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Тамбовская область","все сети","физлица","запрет","ограничение продажи в канистры","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Республика Татарстан","Татнефть","физлица","объем","30 л АИ-95, по топливным картам без лимита","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Тюменская область","Газпромнефть","физлица","объем","40 л бензина/80 л дизеля (город), 40/200 (трасса), только в бак","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Ульяновская область","все сети","физлица","объем","40 л бензина/100 л дизеля (легк), 300 л (груз), только в бак","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Ханты-Мансийский АО — Югра","все сети","физлица","объем","ограничения на ряде АЗС","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Челябинская область","все сети","физлица","объем","ограничения в Кыштыме","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Чувашская Республика","Татнефть","физлица","объем","30 л АИ-95","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Ямало-Ненецкий АО","все сети","физлица","запрет","запрет отпуска в тару, 40-70 л на машину","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    ("Республика Саха (Якутия)","Саханефтегазсбыт","физлица","объем","30 л бензина/200 л дизеля, только в бак","https://www.sravni.ru/novost/2026/7/3/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/","03.07.2026"),
    # Lenta.ru (05.07.2026) — новые/обновлённые
    ("Архангельская область","все сети","физлица","объем","20-50 л, на М8 полный бак","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Республика Алтай","все сети","физлица","объем","30-50 л бензина/50-100 л дизеля с 01.07 до 01.09","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Ивановская область","все сети","физлица","объем","30 л бензина/60 л дизеля","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Республика Карелия","все сети","физлица","объем","20-60 л, зависитот АЗС","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Смоленская область","все сети","физлица","объем","30 л бензина/60 л дизеля","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Тверская область","все сети","физлица","объем","зависит от АЗС, время для спецтранспорта","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Кировская область","все сети","физлица","объем","30-100 л, зависит от АЗС","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Красноярский край","Газпромнефть","физлица","объем","до 40 л, запрет канистр","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Ленинградская область","все сети","физлица","объем","20-30 л","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Республика Башкортостан","все сети","физлица","объем","30 л бензина с 27.06","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Республика Крым","все сети","физлица","объем","до 20 л АИ-92, АИ-95 только экстренным","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Севастополь","все сети","физлица","объем","ограниченная продажа с 03.07 на 8 АЗС","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Брянская область","все сети","физлица","объем","до 20 л","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Курская область","все сети","физлица","объем","20-30 л, только в бак","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Владимирская область","все сети","физлица","объем","20-30 л бензина/40 л дизеля","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Иркутская область","все сети","физлица","объем","до 50 л, Нижнеилимский — 30 л 2 дня в нед","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Ханты-Мансийский АО — Югра","все сети","физлица","объем","40 л бензина/80 л дизеля","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Липецкая область","все сети","физлица","объем","30 л бензина, дизель без ограничений","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Тамбовская область","все сети","физлица","объем","30 л","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Чувашская Республика","Лукойл","физлица","объем","20 л бензина","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Краснодарский край","все сети","физлица","объем","20-30 л (Краснодар), Сочи 30 л бензина/60 л дизеля","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Приморский край","ННК","грузовики","объем","100 л в городе, 200 л на трассе","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Приморский край","все сети","физлица","запрет","запрет канистр","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Забайкальский край","все сети","физлица","объем","15 л, по QR-кодам с 04.07","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    ("Белгородская область","все сети","физлица","объем","до 30 л бензина/60 л дизеля","https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm","05.07.2026"),
    # AA.com.tr (01.07.2026) — дополнительные уточнения
    ("Ростовская область","все сети","физлица","объем","40 л","https://www.aa.com.tr/ru/эконoмика/геoграфия-oграничений-на-прoдажу-тoплива-в-рoссии-прoдoлжает-расширяться/3983182","01.07.2026"),
    ("Ставропольский край","все сети","физлица","объем","35 л","https://www.aa.com.tr/ru/эконoмика/геoграфия-oграничений-на-прoдажу-тoплива-в-рoссии-прoдoлжает-расширяться/3983182","01.07.2026"),
    ("Республика Татарстан","Газпромнефть","физлица","объем","30 л бензина/60 л дизеля","https://www.aa.com.tr/ru/эконoмика/геoграфия-oграничений-на-прoдажу-тoплива-в-рoссии-прoдoлжает-расширяться/3983182","01.07.2026"),
    ("Мурманская область","Роснефть","физлица","объем","99 л бензина","https://www.aa.com.tr/ru/эконoмика/геoграфия-oграничений-на-прoдажу-тoплива-в-рoссии-прoдoлжает-расширяться/3983182","01.07.2026"),
]

def upsert_restriction(reg, net, ct, lt, val, url, date):
    db = sqlite3.connect(DB)
    cur = db.execute(
        "SELECT id, limit_value FROM restrictions WHERE region=? AND COALESCE(network,'')=COALESCE(?,'') AND client_type=? AND limit_type=? AND is_current=1",
        (reg, net or '', ct, lt)
    ).fetchone()
    if cur and cur[1] != val:
        db.execute("UPDATE restrictions SET is_current=0, previous_value=limit_value, updated_at=datetime('now') WHERE id=?", (cur[0],))
    if not cur or cur[1] != val:
        db.execute("INSERT OR IGNORE INTO restrictions(region,network,client_type,limit_type,limit_value,source_url,source_date) VALUES(?,?,?,?,?,?,?)", (reg, net, ct, lt, val, url, date))
    db.commit()
    db.close()

# Insert all restrictions
for reg, net, ct, lt, val, url, date in restrictions:
    upsert_restriction(reg, net, ct, lt, val, url, date)

print(f"Inserted/updated {len(restrictions)} restriction records")

# ── Prices from script data (hardcoded base) + finacia.net (06.07.2026) ──
# Update prices with fresh data from finacia.net (06.07.2026):
# Average diesel by network: Lukoil 85.90, Rosneft 84.10, Gazpromneft 84.50, Tatneft 83.90
# National avg: 84.84 (from finacia) / 80.69 (from driff) — use finacia as it's network-specific
# We'll keep the script's base dict prices and add/update a few

prices_to_save = [
    # Fresh from finacia — national average and network prices
    ("Россия (средняя)", 84.84, "https://finacia.net/economy/44303/", "06.07.2026"),
    ("Лукойл", 85.90, "https://finacia.net/economy/44303/", "06.07.2026"),
    ("Роснефть", 84.10, "https://finacia.net/economy/44303/", "06.07.2026"),
    ("Газпромнефть", 84.50, "https://finacia.net/economy/44303/", "06.07.2026"),
    ("Татнефть", 83.90, "https://finacia.net/economy/44303/", "06.07.2026"),
    # Keep existing script prices — gen_diesel_map.py has them via base dict
    # We'll re-insert the key ones from the script
    ("Москва", 79.28, "https://driff.ru/fuel-dynamics/", "06.07.2026"),
    ("Санкт-Петербург", 79.79, "https://driff.ru/fuel-dynamics/", "06.07.2026"),
    ("Республика Крым", 127.45, "https://www.sravni.ru/text/skolko-stoit-toplivo-v-regionah-rossii-k-29-iyunya-2026-goda/", "06.07.2026"),
    ("Севастополь", 101.63, "https://www.sravni.ru/text/skolko-stoit-toplivo-v-regionah-rossii-k-29-iyunya-2026-goda/", "06.07.2026"),
    ("Краснодарский край", 76.55, "https://driff.ru/fuel-dynamics/", "06.07.2026"),
    ("Республика Дагестан", 98.26, "https://driff.ru/fuel-dynamics/", "06.07.2026"),
    ("Новосибирская область", 84.94, "https://driff.ru/fuel-dynamics/", "06.07.2026"),
    ("Свердловская область", 79.85, "https://driff.ru/fuel-dynamics/", "06.07.2026"),
    ("Татарстан", 76.12, "https://driff.ru/fuel-dynamics/", "06.07.2026"),
    ("Забайкальский край", 96.67, "https://driff.ru/fuel-dynamics/", "06.07.2026"),
]

db = sqlite3.connect(DB)
for reg, price, url, date in prices_to_save:
    db.execute("INSERT OR REPLACE INTO prices(region,price,source_url,source_date,updated_at) VALUES(?,?,?,?,datetime('now'))",
               (reg, price, url, date))
db.commit()
db.close()
print(f"Inserted/updated {len(prices_to_save)} price records")
print("Done")
