#!/usr/bin/env python3
"""Dump restrictions + prices DB to /srv/static/data.json for the site.

Перед выгрузкой запускает normalize_current.py, который выставляет
is_current=1 самой свежей записи по каждому региону+сети+клиенту,
а остальные — is_current=0. Это гарантирует, что данные на карте
всегда актуальны, независимо от того, с каким is_current их вставили.

Формат данных для новой карты (5 уровней жёсткости + лимиты для грузовиков):
{
  "regions": [...],
  "updated": "03.07.2026 15:46 МСК",
  "changelog": "Текст последнего summary из Telegram",
  "changelog_date": "03.07.2026",
  "recent_news": [
    {
      "region": "Москва",
      "network": "Газпромнефть",
      "limit": "60 л",
      "client": "все",
      "source": "https://...",
      "date": "03.07.2026"
    },
    ...
  ]
}

Уровни жёсткости:
  -1 "нет данных" — данные не собраны, ограничения могут быть
   0 "свободно"   — подтверждённое отсутствие ограничений (только при has_source=True)
   1 "мягкие"     — лимиты 100-200 л
   2 "средние"    — лимиты 40-99 л
   3 "жёсткие"    — лимиты < 40 л, только в бак, запрет канистр
   4 "дефицит"    — АЗС закрыты, ЧС
"""
import sqlite3
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta

DB = "/root/diesel_limits/restrictions.db"
OUT = "/srv/static/data.json"

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
    "Республика Татарстан": "Республика Татарстан (Татарстан)",
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
    "Москва и Московская область": "Московская область",
    # ponytail: normalize duplicate names that differ by prefix/format
    "г. Москва": "Москва",
    "г. Санкт-Петербург": "Санкт-Петербург",
    "Чувашская Республика - Чувашия": "Чувашская Республика",
    "Чувашская республика": "Чувашская Республика",
    "Еврейская автономная область": "Еврейская АО",
    "Кемеровская область - Кузбасс": "Кемеровская область",
    "Республика Северная Осетия - Алания": "Республика Северная Осетия — Алания",
    "Удмуртская республика": "Удмуртская Республика",
    "Ханты-Мансийский автономный округ": "Ханты-Мансийский АО - Югра",
    "Ханты-Мансийский автономный округ - Югра": "Ханты-Мансийский АО - Югра",
    "Ханты-Мансийский автономный округ — Югра": "Ханты-Мансийский АО - Югра",
    "Ямало-Ненецкий автономный округ": "Ямало-Ненецкий АО",
    "Свердловская область (Екатеринбург)": "Свердловская область",
    "Челябинская область (Кыштым)": "Челябинская область",
    "Карачаево-Черкесия": "Карачаево-Черкесская Республика",
}


def normalize_region(name):
    if not name:
        return name
    return REGION_ALIASES.get(name.strip(), name.strip())


def normalize_price(val):
    if val is None:
        return None
    try:
        p = float(val)
        return p if 0 < p < 1000 else None
    except (TypeError, ValueError):
        return None


def calc_level(limit_text, has_source=False):
    """Вычисляет уровень жёсткости (-1..4) на основе текста лимита.

    -1 = нет данных (ограничения могут быть, но не подтверждены)
     0 = подтверждённое отсутствие ограничений (нужен has_source=True)
     1-4 = нарастание жёсткости

    ВАЖНО: сначала проверяем жёсткие маркеры, потом мягкие.
    """
    if not limit_text:
        return -1
    l = limit_text.lower()

    # Level 4 — полный дефицит / ЧС / АЗС не работают
    if any(w in l for w in ['закрыт', 'чс', 'дефицит', 'режим чс',
                             'только госслужб', 'только для гос', 'максимальн',
                             'полное ограничение свободн']):
        return 4

    # Level 3 — жёсткие лимиты: только в бак, запрет канистр, < 40 л
    if any(w in l for w in ['только в бак', 'запрет канистр', 'канистр запрещ',
                             'полное ограничение', 'полный запрет']):
        return 3

    # Level 0 — подтверждённая свобода (проверяем после жёстких маркеров,
    # чтобы "свободной" в "ограничение свободной продажи" не сработало)
    if ('без ограничений' in l or 'без лимит' in l or l == 'свободно'):
        return 0 if has_source else -1
    # Отдельное слово "свободно" только если нет "ограничен" рядом
    if 'свободн' in l and 'ограничен' not in l:
        return 0 if has_source else -1

    # Парсим лимиты: поддерживаем диапазоны "20-50 л", "20–50 л", "60/200 л"
    # Берём МИНИМУМ из найденных чисел (минимум = самый жёсткий лимит).
    # ВАЖНО: re.search(r'(\d+)\s*л') находит только число, стоящее НЕПОСРЕДСТВЕННО
    # перед 'л'. В строке "20-50 л" оно найдёт только 50, пропустив 20.
    # Поэтому сначала ищем диапазоны, потом одиночные числа.
    nums = []
    # 1. Диапазоны: 20-50 л, 20–50 л, 20/50 л
    for m in re.finditer(r'(\d+)\s*[-–/]\s*(\d+)\s*л', l):
        nums.append(int(m.group(1)))
        nums.append(int(m.group(2)))
    # 2. Одиночные: 60 л (исключая уже найденные диапазоны)
    l_clean = re.sub(r'\d+\s*[-–/]\s*\d+\s*л', '', l)
    for m in re.finditer(r'(\d+)\s*л', l_clean):
        nums.append(int(m.group(1)))

    if nums:
        min_lim = min(nums)
        if min_lim < 40:
            return 3
        elif min_lim < 100:
            return 2
        else:
            return 1

    # Level 2 — упоминание лимитов/ограничений без конкретных цифр
    if 'лимит' in l or 'огранич' in l:
        return 2

    return -1



def main():
    # Шаг 0: нормализация is_current — самые свежие записи = актуальные
    try:
        subprocess.run(
            [sys.executable, os.path.join(os.path.dirname(__file__), "normalize_current.py")],
            check=True, capture_output=True, text=True
        )
    except Exception as e:
        print(f"⚠ normalize_current не выполнен: {e}")

    db = sqlite3.connect(DB)

    # Цены
    prices = {}
    for r in db.execute("SELECT region, price FROM prices"):
        name = normalize_region(r[0])
        p = normalize_price(r[1])
        if name and p is not None:
            prices[name] = p

    # Ограничения
    restrictions_by_region = {}
    for r in db.execute(
        "SELECT region, network, limit_value, client_type, source_url, source_date "
        "FROM restrictions WHERE is_current=1 "
        "ORDER BY source_date DESC, region"
    ):
        name = normalize_region(r[0])
        if not name:
            continue
        restrictions_by_region.setdefault(name, []).append({
            "network": r[1] or "",
            "limit": r[2] or "",
            "client": r[3] or "",
            "source": r[4] or "",
            "date": r[5] or "—"
        })

    # Изменения цен за неделю
    weekly_changes = {}
    try:
        for r in db.execute(
            "SELECT region, MAX(price) - MIN(price) FROM prices_history "
            "WHERE date >= datetime('now','-7 days') GROUP BY region"
        ):
            name = normalize_region(r[0])
            if name and r[1] is not None:
                weekly_changes[name] = round(float(r[1]), 2)
    except sqlite3.OperationalError:
        pass

    # Последние 10 новостей (без фильтра is_current — все изменения)
    recent_news = []
    try:
        for r in db.execute(
            "SELECT region, network, limit_value, client_type, source_url, source_date "
            "FROM restrictions "
            "ORDER BY source_date DESC, region LIMIT 10"
        ):
            name = normalize_region(r[0])
            if not name:
                continue
            recent_news.append({
                "region": name,
                "network": r[1] or "все сети",
                "limit": r[2] or "",
                "client": r[3] or "все",
                "source": r[4] or "",
                "date": r[5] or "—"
            })
    except sqlite3.OperationalError:
        pass

    # Regions
    regions = []

    # Правило наследования: если у Московской области нет своих ограничений — берём от Москвы
    if "Московская область" not in restrictions_by_region and "Москва" in restrictions_by_region:
        restrictions_by_region["Московская область"] = restrictions_by_region["Москва"]
    # Цену тоже наследуем, если своей нет
    if "Московская область" not in prices and "Москва" in prices:
        prices["Московская область"] = prices["Москва"]

    all_names = set(prices.keys()) | set(restrictions_by_region.keys())
    for name in sorted(all_names):
        price = prices.get(name)
        restricts = restrictions_by_region.get(name, [])
        has_source = any(r.get('source') for r in restricts)
        fiz = [r for r in restricts if r['client'] in ('', 'физлица', 'все', None)]
        ur = [r for r in restricts if r['client'] in ('юридические лица', 'юрлица')]
        if fiz:
            parts = [f"{r['network']}: {r['limit']}" if r['network'] else r['limit']
                     for r in fiz[:2]]
            limit_text = "; ".join(parts)
        else:
            limit_text = "Нет данных"
        if ur:
            truck_limits = [
                {"network": r["network"] or "все сети",
                 "limit": r["limit"] or "Без ограничений",
                 "client": r["client"] or "все"}
                for r in ur
            ]
        else:
            truck_limits = [
                {"network": "все сети", "limit": "нет данных", "client": "все"}
            ]
        level = calc_level(limit_text, has_source=has_source)
        regions.append({
            "region": name,
            "level": level,
            "price": price,
            "limit_text": limit_text,
            "truck_limits": truck_limits,
            "weekly_change": weekly_changes.get(name)
        })

    # Changelog — читает из файла, который пишет publish-крон
    CHANGELOG_FILE = "/srv/static/changelog_latest.txt"
    changelog = ""
    changelog_date = ""
    try:
        with open(CHANGELOG_FILE) as f:
            raw = f.read().strip()
        if raw:
            lines = raw.split("\n", 1)
            changelog = lines[0]
            changelog_date = lines[1].strip() if len(lines) > 1 else ""
    except (FileNotFoundError, OSError):
        pass
    if not changelog:
        changelog = "За сутки изменений нет"
        changelog_date = datetime.now(timezone(timedelta(hours=3))).strftime("%d.%m.%Y %H:%M")

    db.close()

    msk = timezone(timedelta(hours=3))
    updated = datetime.now(msk).strftime("%d.%m.%Y %H:%M МСК")

    data = {
        "regions": regions,
        "updated": updated,
        "changelog": changelog,
        "changelog_date": changelog_date,
        "recent_news": recent_news,
        # Обратная совместимость
        "prices": {r["region"]: r["price"] for r in regions if r["price"] is not None},
        "restrictions": [
            {"region": r["region"], "network": t["network"], "limit": t["limit"],
             "client": t["client"], "source": "", "date": "—"}
            for r in regions for t in r["truck_limits"]
        ]
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    os.chmod(OUT, 0o644)

    # ponytail: copy index.html to /srv/static/ so git pulls take effect
    index_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    index_dst = "/srv/static/index.html"
    if os.path.exists(index_src):
        import shutil
        shutil.copy2(index_src, index_dst)
        os.chmod(index_dst, 0o644)

    print(f"dumped {OUT}: {len(regions)} regions, {len(recent_news)} recent news")
    if changelog:
        print(f"  changelog: {changelog[:80]}...")
    from collections import Counter
    c = Counter(r["level"] for r in regions)
    labels = ["нет данных", "свободно", "мягкие", "средние", "жёсткие", "дефицит"]
    for lv in range(-1, 5):
        print(f"  Уровень {lv} ({labels[lv+1]}): {c.get(lv, 0)} регионов")


if __name__ == "__main__":
    main()
