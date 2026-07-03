#!/usr/bin/env python3
"""Dump restrictions + prices DB to /srv/static/data.json for the site.

Формат данных для новой карты (5 уровней жёсткости + лимиты для грузовиков):
{
  "regions": [
    {
      "region": "Москва",
      "level": 2,
      "price": 79.00,
      "limit_text": "Лимит 60 л в городе / 200 л на трассе",
      "truck_limits": [...],
      "weekly_change": null
    },
    ...
  ],
  "updated": "03.07.2026 15:46 МСК"
}

Уровни жёсткости:
  0 "свободно"   — нет ограничений
  1 "мягкие"     — лимиты 100-200 л
  2 "средние"    — лимиты 40-99 л
  3 "жёсткие"    — лимиты < 40 л, только в бак, запрет канистр
  4 "дефицит"    — АЗС закрыты, ЧС
"""
import sqlite3
import json
import os
import re
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


def calc_level(limit_text):
    """Вычисляет уровень жёсткости (0-4) на основе текста лимита."""
    if not limit_text:
        return 0
    l = limit_text.lower()
    if any(w in l for w in ['закрыт', 'чс', 'дефицит', 'режим чс']):
        return 4
    if 'без ограничений' in l or 'свободн' in l:
        return 0
    if 'только в бак' in l or 'запрет канистр' in l or 'канистр запрещ' in l:
        return 3
    m = re.search(r'(\d+)\s*л', l)
    if m:
        lim = int(m.group(1))
        if lim < 40:
            return 3
        elif lim < 100:
            return 2
        else:
            return 1
    if 'лимит' in l or 'огранич' in l:
        return 2
    return 0


def main():
    db = sqlite3.connect(DB)

    prices = {}
    for r in db.execute("SELECT region, price FROM prices"):
        name = normalize_region(r[0])
        p = normalize_price(r[1])
        if name and p is not None:
            prices[name] = p

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

    db.close()

    regions = []
    all_names = set(prices.keys()) | set(restrictions_by_region.keys())
    for name in sorted(all_names):
        price = prices.get(name)
        restricts = restrictions_by_region.get(name, [])
        if restricts:
            parts = [f"{r['network']}: {r['limit']}" if r['network'] else r['limit']
                     for r in restricts[:2]]
            limit_text = "; ".join(parts) if parts else "Без ограничений"
        else:
            limit_text = "Без ограничений"
        level = calc_level(limit_text)
        truck_limits = [
            {"network": r["network"] or "все сети",
             "limit": r["limit"] or "без ограничений",
             "client": r["client"] or "все"}
            for r in restricts
        ]
        regions.append({
            "region": name,
            "level": level,
            "price": price,
            "limit_text": limit_text,
            "truck_limits": truck_limits,
            "weekly_change": weekly_changes.get(name)
        })

    msk = timezone(timedelta(hours=3))
    updated = datetime.now(msk).strftime("%d.%m.%Y %H:%M МСК")

    data = {
        "regions": regions,
        "updated": updated,
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

    print(f"dumped {OUT}: {len(regions)} regions")
    from collections import Counter
    c = Counter(r["level"] for r in regions)
    labels = ["свободно", "мягкие", "средние", "жёсткие", "дефицит"]
    for lv in range(5):
        print(f"  Уровень {lv} ({labels[lv]}): {c.get(lv, 0)} регионов")


if __name__ == "__main__":
    main()
