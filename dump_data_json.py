#!/usr/bin/env python3
"""Dump restrictions + prices DB to /srv/static/data.json for the site.

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
import urllib.request
from datetime import datetime, timezone, timedelta

DB = "/root/diesel_limits/restrictions.db"
OUT = "/srv/static/data.json"
TG_CHANNEL = "disel_limits_update"  # без @

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


def calc_level(limit_text, has_source=False):
    """Вычисляет уровень жёсткости (-1..4) на основе текста лимита.

    -1 = нет данных (ограничения могут быть, но не подтверждены)
     0 = подтверждённое отсутствие ограничений (нужен has_source=True)
     1-4 = нарастание жёсткости
    """
    if not limit_text:
        return -1
    l = limit_text.lower()

    if any(w in l for w in ['закрыт', 'чс', 'дефицит', 'режим чс']):
        return 4

    if 'без ограничений' in l or 'свободн' in l or 'без лимит' in l:
        return 0 if has_source else -1

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

    return -1


def fetch_tg_summary():
    """Получает последний пост из Telegram-канала (через публичный t.me/s/...).

    Возвращает (text, date_str) или (None, None) при ошибке.
    Не требует Telegram API токена — использует публичную веб-версию канала.
    """
    url = f"https://t.me/s/{TG_CHANNEL}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")

        # Простая регэксп-парсинг: ищем последний блок сообщения
        # t.me/s/... отдаёт HTML с классами tgme_widget_message_text
        msgs = re.findall(
            r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>',
            html, re.DOTALL
        )
        if not msgs:
            return None, None

        # Берём последнее (в t.me/s новые внизу)
        last = msgs[-1]
        # Очистка HTML-тегов
        text = re.sub(r'<br\s*/?>', '\n', last)
        text = re.sub(r'<[^>]+>', '', text)
        text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        text = text.strip()

        # Дата
        dates = re.findall(
            r'<time datetime="([^"]+)"',
            html
        )
        date_str = ""
        if dates:
            try:
                dt = datetime.fromisoformat(dates[-1].replace("Z", "+00:00"))
                msk = timezone(timedelta(hours=3))
                date_str = dt.astimezone(msk).strftime("%d.%m.%Y %H:%M")
            except Exception:
                date_str = dates[-1]

        return text, date_str

    except Exception as e:
        print(f"⚠ Не удалось получить Telegram-пост: {e}")
        return None, None


def main():
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

    db.close()

    # Regions
    regions = []
    all_names = set(prices.keys()) | set(restrictions_by_region.keys())
    for name in sorted(all_names):
        price = prices.get(name)
        restricts = restrictions_by_region.get(name, [])
        has_source = any(r.get('source') for r in restricts)
        if restricts:
            parts = [f"{r['network']}: {r['limit']}" if r['network'] else r['limit']
                     for r in restricts[:2]]
            limit_text = "; ".join(parts)
            truck_limits = [
                {"network": r["network"] or "все сети",
                 "limit": r["limit"] or "Без ограничений",
                 "client": r["client"] or "все"}
                for r in restricts
            ]
        else:
            limit_text = "Нет данных"
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

    # Telegram summary (блок 1 — лента изменений)
    changelog, changelog_date = fetch_tg_summary()
    if not changelog:
        changelog = "Лента обновлений временно недоступна. См. канал @disel_limits_update"
        changelog_date = ""

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
