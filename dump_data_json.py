#!/usr/bin/env python3
"""Dump restrictions + prices DB to /srv/static/data.json for the site.

Улучшения:
- Нормализация имён регионов к каноничным (как в russia_topo.json).
- Добавлено поле client (для отображения в popup).
- Дата обновления с указанием таймзоны (MSK).
- Валидация цен (только числа > 0).
"""
import sqlite3
import json
import os
from datetime import datetime, timezone, timedelta

DB = "/root/diesel_limits/restrictions.db"
OUT = "/srv/static/data.json"

# Каноничные имена регионов России (как в russia_topo.json)
# Ключ — короткое/нестандартное имя из БД, значение — каноничное.
REGION_ALIASES = {
    "Дагестан": "Республика Дагестан",
    "Якутия": "Республика Саха (Якутия)",
    "Чечня": "Чеченская Республика",
    "Крым": "Республика Крым",
    "Севастополь": "город федерального значения Севастополь",
    "ХМАО": "Ханты-Мансийский АО - Югра",
    "ЯНАО": "Ямало-Ненецкий АО",
    "НАО": "Ненецкий АО",
    "Чукотка": "Чукотский АО",
    "Кабардино-Балкария": "Кабардино-Балкарская Республика",
    "Карачаево-Черкесия": "Карачаево-Черкесская Республика",
    "Северная Осетия": "Республика Северная Осетия - Алания",
    "Адыгея": "Республика Адыгея (Адыгея)",
    "Татарстан": "Республика Татарстан (Татарстан)",
    "Башкортостан": "Республика Башкортостан",
    "Бурятия": "Республика Бурятия",
    "Тыва": "Республика Тыва",
    "Хакасия": "Республика Хакасия",
    "Алтай": "Республика Алтай",
    "Калмыкия": "Республика Калмыкия",
    "Ингушетия": "Республика Ингушетия",
    "Марий Эл": "Республика Марий Эл",
    "Мордовия": "Республика Мордовия",
    "Карелия": "Республика Карелия",
    "Коми": "Республика Коми",
    "Удмуртия": "Удмуртская Республика",
    "Чувашия": "Чувашская Республика - Чувашия",
    "Камчатка": "Камчатский край",
    "Приморье": "Приморский край",
    "Хабаровск": "Хабаровский край",
    "Забайкалье": "Забайкальский край",
    "Пермь": "Пермский край",
    "Краснодарск": "Краснодарский край",
    "Ставрополь": "Ставропольский край",
    "ЕАО": "Еврейская АО",
}


def normalize_region(name):
    """Приводит короткое имя региона к каноничному виду."""
    if not name:
        return name
    return REGION_ALIASES.get(name.strip(), name.strip())


def normalize_price(val):
    """Валидация цены: возвращает float или None."""
    if val is None:
        return None
    try:
        p = float(val)
        return p if 0 < p < 1000 else None
    except (TypeError, ValueError):
        return None


db = sqlite3.connect(DB)

prices = {}
for r in db.execute("SELECT region, price FROM prices"):
    name = normalize_region(r[0])
    p = normalize_price(r[1])
    if name and p is not None:
        prices[name] = p

restrictions = []
for r in db.execute(
    "SELECT region, network, limit_value, client_type, source_url, source_date "
    "FROM restrictions WHERE is_current=1 "
    "ORDER BY source_date DESC, region"
):
    name = normalize_region(r[0])
    if not name:
        continue
    restrictions.append({
        "region": name,
        "network": r[1] or "",
        "limit": r[2] or "",
        "client": r[3] or "",
        "source": r[4] or "",
        "date": r[5] or "—"
    })

# Московское время (UTC+3) — серверное время может быть в UTC
msk = timezone(timedelta(hours=3))
updated = datetime.now(msk).strftime("%d.%m.%Y %H:%M МСК")

data = {
    "prices": prices,
    "restrictions": restrictions,
    "updated": updated
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
os.chmod(OUT, 0o644)

print(f"dumped {OUT}: {len(prices)} regions, {len(restrictions)} restrictions")
