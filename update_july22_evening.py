#!/usr/bin/env python3
"""Update diesel map prices + insert prices + insert restrictions (22 July 2026)."""
import sqlite3, json, os, sys
from datetime import datetime

TODAY = "22.07.2026"
DB = "/root/diesel_limits/restrictions.db"
ROOT = "/root/diesel_limits"

# ── 1. New diesel prices from petrolplus.ru (22 Jul 2026) ──
new_prices = {
    "Москва": 79.98,
    "Санкт-Петербург": 80.3,
    "Алтайский край": 81.02,
    "Амурская область": 89.32,
    "Архангельская область": 83.29,
    "Астраханская область": 77.36,
    "Белгородская область": 77.05,
    "Брянская область": 75.63,
    "Владимирская область": 78.07,
    "Волгоградская область": 77.11,
    "Вологодская область": 84.33,
    "Воронежская область": 77.49,
    "Еврейская АО": 89.41,
    "Забайкальский край": 98.8,
    "Ивановская область": 76.63,
    "Иркутская область": 94.0,
    "Кабардино-Балкарская Республика": 76.25,
    "Калининградская область": 83.0,
    "Калужская область": 76.55,
    "Камчатский край": 96.22,
    "Карачаево-Черкесская Республика": 74.95,
    "Кемеровская область": 80.23,
    "Кировская область": 86.0,
    "Костромская область": 79.19,
    "Краснодарский край": 77.05,
    "Красноярский край": 92.87,
    "Курганская область": 80.4,
    "Курская область": 77.05,
    "Ленинградская область": 80.3,
    "Липецкая область": 76.0,
    "Магаданская область": 107.1,
    "Московская область": 78.76,
    "Мурманская область": 87.95,
    "Ненецкий АО": 86.77,
    "Нижегородская область": 77.87,
    "Новгородская область": 80.23,
    "Новосибирская область": 85.0,
    "Омская область": 79.36,
    "Оренбургская область": 79.75,
    "Орловская область": 75.32,
    "Пензенская область": 78.2,
    "Пермский край": 81.99,
    "Приморский край": 88.87,
    "Псковская область": 81.1,
    "Республика Адыгея": 76.0,
    "Республика Алтай": 98.03,
    "Республика Башкортостан": 78.0,
    "Республика Бурятия": 85.6,
    "Республика Дагестан": 111.17,
    "Республика Ингушетия": 76.4,
    "Республика Калмыкия": 76.5,
    "Республика Карелия": 84.21,
    "Республика Коми": 81.05,
    "Республика Крым": 139.15,
    "Республика Марий Эл": 99.66,
    "Республика Мордовия": 78.6,
    "Республика Саха (Якутия)": 107.1,
    "Республика Северная Осетия — Алания": 74.45,
    "Республика Татарстан": 80.55,
    "Республика Тыва": 96.0,
    "Республика Хакасия": 95.0,
    "Ростовская область": 77.15,
    "Рязанская область": 76.66,
    "Самарская область": 76.75,
    "Саратовская область": 78.05,
    "Сахалинская область": 95.56,
    "Свердловская область": 80.19,
    "Севастополь": 150.49,
    "Смоленская область": 77.25,
    "Ставропольский край": 77.25,
    "Тамбовская область": 76.0,
    "Тверская область": 79.65,
    "Томская область": 83.23,
    "Тульская область": 77.15,
    "Тюменская область": 80.97,
    "Удмуртская Республика": 79.62,
    "Ульяновская область": 77.2,
    "Хабаровский край": 88.54,
    "Ханты-Мансийский АО — Югра": 87.51,
    "Челябинская область": 79.77,
    "Чеченская Республика": 85.0,
    "Чувашская Республика": 76.56,
    "Чукотский АО": 78.0,
    "Ямало-Ненецкий АО": 84.84,
    "Ярославская область": 78.11,
}

SOURCE_URL = "https://www.petrolplus.ru/fuelindex/"
SOURCE_DATE = TODAY

# ── 2. Patch base prices in gen_diesel_map.py ──
import re
with open(f"{ROOT}/gen_diesel_map.py", "r") as f:
    content = f.read()

# Replace the base dict in-place
lines = content.split("\n")
in_base = False
base_start = None
base_end = None
for i, line in enumerate(lines):
    if 'base = {' in line:
        in_base = True
        base_start = i
    if in_base and line.strip() == '}':
        base_end = i
        break

if base_start is not None and base_end is not None:
    new_base_lines = ["# ── PetrolPlus цены (22 июля 2026) — основной источник ──", "base = {"]
    for r, p in sorted(new_prices.items(), key=lambda x: x[0]):
        new_base_lines.append(f'    "{r}":{p},'.replace(",", ","))
    new_base_lines.append("}")
    lines[base_start:base_end+1] = new_base_lines
    content = "\n".join(lines)
    with open(f"{ROOT}/gen_diesel_map.py", "w") as f:
        f.write(content)
    print(f"✓ Updated gen_diesel_map.py with {len(new_prices)} prices")
else:
    print("✗ Could not find base dict in gen_diesel_map.py")

# ── 3. Insert prices into DB ──
db = sqlite3.connect(DB)
for region, price in new_prices.items():
    db.execute(
        "INSERT OR REPLACE INTO prices (region, price, source_url, source_date, updated_at) VALUES (?, ?, ?, ?, datetime('now'))",
        (region, price, SOURCE_URL, SOURCE_DATE)
    )
db.commit()
print(f"✓ Inserted {len(new_prices)} prices into DB")

# ── 4. Insert prices into history ──
inserted = 0
for r in db.execute("SELECT region, price FROM prices WHERE price IS NOT NULL"):
    region, price = r
    try:
        db.execute("INSERT OR IGNORE INTO prices_history (region, date, price) VALUES (?, ?, ?)",
                   (region, TODAY, float(price)))
        inserted += 1
    except:
        pass
db.commit()
print(f"✓ Inserted {inserted} history records")

# ── 5. Insert restrictions from research ──
restrictions = [
    # (region, city, network, client_type, limit_type, limit_value, prev_value, source_url, source_date)
    ("Адыгея", None, None, "Все", "рекомендация", "Временно воздержаться от поездок на личных авто", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "07.07.2026"),
    ("Краснодарский край", None, "Все АЗС", "Все", "объем", "ДТ: 30-60 л на авто", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "07.07.2026"),
    ("Приморский край", None, "Все АЗС", "Грузовики", "объем", "ДТ: до 100 л (город), до 200 л (трасса)", None, "https://primorsky.ru/news/318665", "29.06.2026"),
    ("Псковская область", None, None, "Все", "объем", "ДТ: до 40 л", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "07.07.2026"),
    ("Удмуртская Республика", None, None, "Все", "объем", "ДТ: до 40 л", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "07.07.2026"),
    ("Кировская область", None, "Некоторые АЗС", "Все", "объем", "ДТ: до 100 л", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "07.07.2026"),
    ("Ульяновская область", None, "Некоторые АЗС", "Все", "объем", "ДТ: до 100 л", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "07.07.2026"),
    ("Дагестан", None, "Все АЗС", "Физлица", "объем", "ДТ: 50 л", None, "https://tass.ru/obschestvo/27855585", "25.06.2026"),
    ("Воронежская область", "Воронеж", "Лукойл", "Все", "объем", "ДТ: 60 л", None, "https://www.aa.com.tr/ru/.../3983182", "01.07.2026"),
    ("Калининградская область", None, "Крупные сети", "Все", "объем", "ДТ: 60 л", None, "https://www.aa.com.tr/ru/.../3983182", "01.07.2026"),
    ("Татарстан", None, "Газпромнефть", "Все", "объем", "ДТ: 60 л", None, "https://www.aa.com.tr/ru/.../3983182", "01.07.2026"),
    ("Мурманская область", None, "Лукойл", "Все", "объем", "ДТ: 60 л", None, "https://www.aa.com.tr/ru/.../3983182", "01.07.2026"),
    ("Мурманская область", None, "Газпромнефть", "Все", "объем", "ДТ: 30 л", None, "https://www.aa.com.tr/ru/.../3983182", "01.07.2026"),
    ("Омская область", None, "Все АЗС", "Все", "объем", "ДТ: 80 л (город), 200 л (трасса)", None, "https://www.aa.com.tr/ru/.../3983182", "01.07.2026"),
    ("Кемеровская область", None, "Газпромнефть", "Все", "объем", "ДТ: 80 л (город), 200 л (трасса)", None, "https://www.aa.com.tr/ru/.../3983182", "01.07.2026"),
    ("Республика Саха (Якутия)", None, "Саханефтегазсбыт", "Все", "объем", "ДТ: 200 л; запрет канистры", None, "https://www.aa.com.tr/ru/.../3983182", "01.07.2026"),
    ("Белгородская область", None, "Лукойл", "Физлица", "объем", "ДТ: 60 л", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "03.07.2026"),
    ("Владимирская область", None, "АЗС региона", "Физлица", "объем", "ДТ: 40 л", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "18.06.2026"),
    ("Карелия", None, "Ряд АЗС", "Все", "объем", "ДТ: 20-60 л; запрет канистры", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "04.07.2026"),
    ("Красноярский край", None, "Газпромнефть", "Все", "объем", "ДТ: 40-80 л (город), 200 л (трасса)", None, "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "01.07.2026"),
    ("Пензенская область", None, "Все АЗС", "Физлица", "объем", "ДТ: 200 л", None, "https://www.aa.com.tr/ru/.../3983182", "23.06.2026"),
    ("Забайкальский край", None, None, "Все", "объем", "Бензин: 15 л (дефицит)", None, "https://www.aa.com.tr/ru/.../3983182", "01.07.2026"),
    ("Самарская область", None, "Все АЗС", "Легковые", "объем", "ДТ: 100 л; запрет канистры", None, "https://www.kommersant.ru/doc/8763813", "24.06.2026"),
    ("Липецкая область", None, "Все АЗС", "Все", "объем", "Бензин: 30 л (на ДТ нет лимитов)", None, "https://rtvi.com/news/kak-minimum-v-22-regionah-vlasti-vveli-ogranicheniya-na-prodazhu-benzina/", "24.06.2026"),
    ("Новосибирская область", None, "Все АЗС (рекомендация)", "Все", "объем", "ДТ: 80 л", None, "https://rtvi.com/news/kak-minimum-v-22-regionah-vlasti-vveli-ogranicheniya-na-prodazhu-benzina/", "26.06.2026"),
    ("Мордовия", None, "Все АЗС", "Все", "объем", "ДТ: 60 л (легковые), 300 л (грузовые)", None, "https://rtvi.com/news/kak-minimum-v-22-regionah-vlasti-vveli-ogranicheniya-na-prodazhu-benzina/", "23.06.2026"),
    ("Москва", None, "Газпромнефть", "Все", "объем", "ДТ: 60 л (город), 200 л (трасса); запрет канистры", None, "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "12.07.2026"),
    ("Московская область", None, "Лукойл/Teboil", "Все", "объем", "ДТ: 60 л (Teboil 100 л)", None, "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "12.07.2026"),
    ("Ростовская область", None, "Все АЗС", "Все", "объем", "ДТ: 60 л (легковые), 200 л (грузовые), 300 л (автобусы)", None, "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "12.07.2026"),
    ("Республика Крым", None, "Гос. АЗС", "Все", "запрет", "Топливо только экстренным службам", None, "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "12.07.2026"),
    ("Вологодская область", None, "Лукойл", "Все", "объем", "ДТ: 60 л (город), 200 л (трасса)", None, "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "23.06.2026"),
    ("Самарская область", None, "Все АЗС", "Легковые", "объем", "ДТ: 100 л; запрет канистры", None, "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "24.06.2026"),
    ("Томская область", None, "Ряд АЗС (северные районы)", "Все", "объем", "ДТ: до 80 л", None, "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "12.07.2026"),
    ("Республика Алтай", None, "Все АЗС (контроль)", "Все", "объем", "ДТ: 50-100 л/сутки; по СТС", None, "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "09.07.2026"),
    ("Астраханская область", None, "Все АЗС", "Все", "время", "По номерам (чёт/нечет)", None, "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "09.07.2026"),
    ("Кировская область", None, "АЗС Движение", "Все", "объем", "ДТ: до 100 л; заправка по номерам", None, "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "11.07.2026"),
    ("Брянская область", None, "Все АЗС", "Все", "запрет", "Запрет продажи в канистры", None, "https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/", "01.07.2026"),
]

# Mark old current restrictions as not current
db.execute("UPDATE restrictions SET is_current = 0")
print("✓ Marked old restrictions as not current")

# Insert new restrictions
inserted_r = 0
for r in restrictions:
    region, city, network, client_type, limit_type, limit_value, prev_val, url, date = r
    # Check if similar already exists
    existing = db.execute(
        "SELECT id FROM restrictions WHERE region=? AND limit_value=? AND is_current=1",
        (region, limit_value)
    ).fetchone()
    if existing:
        continue
    db.execute(
        "INSERT INTO restrictions (region, city, network, client_type, limit_type, limit_value, previous_value, source_url, source_date, is_current) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
        (region, city, network, client_type, limit_type, limit_value, prev_val, url, date)
    )
    inserted_r += 1
db.commit()
print(f"✓ Inserted {inserted_r} new restrictions")

# ── 6. Verify ──
counts = {}
counts['prices'] = db.execute("SELECT COUNT(*) FROM prices").fetchone()[0]
counts['active'] = db.execute("SELECT COUNT(*) FROM restrictions WHERE is_current=1").fetchone()[0]
counts['total_r'] = db.execute("SELECT COUNT(*) FROM restrictions").fetchone()[0]
counts['changes'] = db.execute("SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL").fetchone()[0]
try:
    counts['history'] = len(os.listdir("/srv/static/history"))
except:
    counts['history'] = 0

db.close()
print(f"✓ DB: prices={counts['prices']}, active_restrictions={counts['active']}, total_restrictions={counts['total_r']}, changes={counts['changes']}, history={counts['history']}")

# Print summary
print(f"\n{'='*50}")
print(f"ОБНОВЛЕНИЕ 22.07.2026 ЗАВЕРШЕНО")
print(f"{'='*50}")
