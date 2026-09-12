#!/usr/bin/env python3
"""Insert latest diesel restrictions from July 31 search sweep."""
import sqlite3
from datetime import datetime

DB = "/root/diesel_limits/restrictions.db"
SRC_DATE = "2026-07-31"
SRC_UPDATED = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

new_restrictions = [
    # === LATEST CHANGES (end of July) ===
    ("Омская область", None, None, "физлица", "отмена", "лимиты полностью отменены губернатором 28.07.2026", "https://tass.ru/obschestvo/27960199"),
    ("Москва", None, "Лукойл", "физлица", "отмена", "лимиты полностью отменены в Московском регионе", "https://tass.ru/obschestvo/27960199"),
    ("Москва", None, "Teboil", "физлица", "отмена", "лимиты отменены", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Санкт-Петербург", None, None, "физлица", "отмена", "ограничений практически не осталось", "https://tass.ru/obschestvo/27960199"),
    ("Ленинградская область", None, None, "физлица", "отмена", "лимиты увеличены: ряд компаний поднял лимит АИ-92 до 40-60 л, АИ-95 до 40 л", "https://finance.mail.ru/article/nu-vot-i-vse-v-kakih-regionah-nachali-snimat-ogranicheniya-na-prodazhu-benzina-i-dizelya-69219723/"),
    ("Республика Карелия", None, None, "физлица", "повышение", "лимит бензина повышен до 40 л; дизель 60 л; большегрузы 250 л дизеля", "https://finance.mail.ru/article/nu-vot-i-vse-v-kakih-regionah-nachali-snimat-ogranicheniya-na-prodazhu-benzina-i-dizelya-69219723/"),
    ("Республика Адыгея", None, None, "физлица", "повышение", "лимит увеличен до 40 л (с 20-30 л) с 21.07", "https://finance.mail.ru/article/nu-vot-i-vse-v-kakih-regionah-nachali-snimat-ogranicheniya-na-prodazhu-benzina-i-dizelya-69219723/"),
    ("Вологодская область", None, "Лукойл", "физлица", "повышение", "лимит увеличен с 30 до 40 л (18.07); дизель 60-200 л", "https://finance.mail.ru/article/nu-vot-i-vse-v-kakih-regionah-nachali-snimat-ogranicheniya-na-prodazhu-benzina-i-dizelya-69219723/"),
    ("Саратовская область", None, None, "физлица", "повышение", "лимит увеличен до 40 л (27.07)", "https://finance.mail.ru/article/nu-vot-i-vse-v-kakih-regionah-nachali-snimat-ogranicheniya-na-prodazhu-benzina-i-dizelya-69219723/"),
    ("Республика Крым", None, None, "все", "частичная отмена", "свободная продажа бензина и дизеля на 99 АЗС (с 11.07)", "https://finance.mail.ru/article/nu-vot-i-vse-v-kakih-regionah-nachali-snimat-ogranicheniya-na-prodazhu-benzina-i-dizelya-69219723/"),
    ("Севастополь", None, None, "физлица", "частичная отмена", "ограничения сняты на 9 АЗС; АИ-95 Ultra и ДТ Ultra в свободной продаже", "https://finance.mail.ru/article/nu-vot-i-vse-v-kakih-regionah-nachali-snimat-ogranicheniya-na-prodazhu-benzina-i-dizelya-69219723/"),
    ("Псковская область", None, None, "физлица", "повышение", "отменен временной график (14:00-24:00); рекомендовано увеличить до 30+ л", "https://finance.mail.ru/article/nu-vot-i-vse-v-kakih-regionah-nachali-snimat-ogranicheniya-na-prodazhu-benzina-i-dizelya-69219723/"),
    
    # === DIESEL-SPECIFIC RESTRICTIONS (compiled from latest sources) ===
    ("Алтай", None, None, "физлица", "объем", "до 50 л дизеля (Горно-Алтайск); до 100 л (остальные); канистры до 10 л", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Архангельская область", None, None, "физлица", "объем", "до 50 л дизеля на большинстве АЗС", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Белгородская область", None, None, "физлица", "объем", "до 60 л дизеля; запрет на канистры", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/"),
    ("Владимирская область", None, None, "физлица", "объем", "до 40 л дизеля; утренние часы для спецслужб (7:00-10:00)", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/"),
    ("Воронежская область", None, "Лукойл", "физлица", "объем", "до 60 л дизеля (город); до 200 л (трасса)", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Дагестан", None, None, "физлица", "объем", "до 50 л дизеля; только в бак", "https://tass.ru/obschestvo/27855585"),
    ("Ивановская область", None, None, "физлица", "объем", "до 60-200 л дизеля; только в бак", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Калининградская область", None, None, "физлица", "объем", "до 60 л дизеля; запрет на канистры", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Карелия", None, None, "физлица", "объем", "до 60 л дизеля; большегрузы до 250 л", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Кемеровская область", None, "Газпромнефть/Лукойл", "физлица", "объем", "до 80 л дизеля; трассы до 200 л", "https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm"),
    ("Краснодарский край", None, None, "физлица", "объем", "30-60 л дизеля; только в бак", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/"),
    ("Курганская область", None, None, "физлица", "объем", "до 80 л дизеля (город); до 200 л (трасса); только в бак", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Мордовия", None, None, "физлица", "объем", "до 60 л дизеля (легковые); до 300 л (грузовые); заправка по номерам", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Москва", None, "Газпромнефть", "физлица", "объем", "до 60 л дизеля; трассы до 200 л; только в бак", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Мурманская область", None, "Лукойл", "физлица", "объем", "до 60 л дизеля", "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/"),
    ("Мурманская область", None, "Газпромнефть", "физлица", "объем", "до 60 л дизеля по топливным картам", "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/"),
    ("Новосибирская область", None, None, "физлица", "объем", "до 60 л дизеля", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Пензенская область", None, None, "физлица", "объем", "до 200 л дизеля; только в бак", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Приморский край", None, None, "грузовики", "объем", "до 100 л дизеля (город); до 200 л (трасса)", "https://primorsky.ru/news/318665"),
    ("Псковская область", None, None, "физлица", "объем", "до 40 л дизеля", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/"),
    ("Ростовская область", None, None, "физлица", "объем", "до 60 л дизеля (легковые); грузовики до 200 л; автобусы до 300 л", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Самарская область", None, None, "физлица", "объем", "до 100 л дизеля (легковые); грузовики до 300 л; только в бак", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Татарстан", None, "Татнефть", "физлица", "объем", "до 60 л дизеля (легковые); грузовики до 300 л; топливные карты без лимита", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Томская область", None, None, "физлица", "объем", "до 80 л дизеля на некоторых АЗС", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Тюменская область", None, "Газпромнефть", "физлица", "объем", "до 80 л дизеля (город); до 200 л (трасса); только в бак", "https://www.kommersant.ru/doc/8763676"),
    ("Удмуртия", None, None, "физлица", "объем", "до 40 л дизеля", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/"),
    ("Ульяновская область", None, None, "физлица", "объем", "до 100 л дизеля (легковые); грузовики до 300 л; только в бак", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Челябинская область", None, "Татнефть", "физлица", "объем", "до 60 л дизеля", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Чувашия", None, None, "грузовики", "объем", "до 300 л дизеля для грузовиков и коммунальной техники", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Якутия", None, None, "физлица", "объем", "до 200 л дизеля; запрет на канистры; по топливным картам", "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/"),
    ("ХМАО", None, None, "физлица", "объем", "60-80 л дизеля на АЗС в городе", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/"),
    ("ЯНАО", None, None, "физлица", "объем", "запрет на отпуск топлива в тару; 40-70 л на машину на частных АЗС", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Забайкальский край", None, None, "физлица", "объем", "до 15 л бензина; QR-коды через бота", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Башкортостан", None, None, "физлица", "объем", "до 30 л бензина; только в бак", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    ("Калмыкия", None, None, "физлица", "объем", "до 30 л бензина в один бак", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
    
    # === FEDERAL-LEVEL MEASURES ===
    ("Российская Федерация", None, None, "все", "запрет", "полный запрет экспорта дизельного топлива до 31 июля 2026 (продлен на производителей)", "https://novayagazeta.ru/articles/2026/07/13/menshe-ezdit-budete"),
    ("Российская Федерация", None, None, "все", "другое", "постановление №819: разрешен выпуск дизеля с серой до 350 мг/кг (Евро-3) до конца 2026", "https://novayagazeta.ru/articles/2026/07/13/menshe-ezdit-budete"),
    ("Российская Федерация", None, None, "все", "другое", "ФАС возбудила дела против 6 независимых АЗС в Московской области за рост цен", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/"),
]

db = sqlite3.connect(DB)
inserted, updated = 0, 0
for r in new_restrictions:
    region, city, network, client_type, limit_type, limit_value, source_url = r
    
    if network is None:
        existing = db.execute(
            "SELECT id, limit_value FROM restrictions WHERE region=? AND network IS NULL AND client_type=? AND limit_type=?",
            (region, client_type, limit_type)
        ).fetchone()
    else:
        existing = db.execute(
            "SELECT id, limit_value FROM restrictions WHERE region=? AND network=? AND client_type=? AND limit_type=?",
            (region, network, client_type, limit_type)
        ).fetchone()
    
    if existing:
        if existing[1] != limit_value:
            db.execute(
                "UPDATE restrictions SET city=?, limit_value=?, previous_value=?, source_url=?, source_date=?, is_current=1, updated_at=? WHERE id=?",
                (city, limit_value, existing[1], source_url, SRC_DATE, SRC_UPDATED, existing[0])
            )
            updated += 1
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
