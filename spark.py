"""Чистые функции агрегации для дизель-лимитов.

Без I/O, без обращения к БД — только обработка списков.
Используется dump_data_json.py (price_spark) и dump_history.py (полная история).
"""
from datetime import datetime, timedelta


def _parse_date(s):
    """'YYYY-MM-DD' → datetime.date. None/unparseable → None."""
    if not s:
        return None
    try:
        return datetime.strptime(str(s).strip(), "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def build_price_spark(rows, days=30, max_points=12):
    """Агрегирует историю цен в массив для спарклайна.

    rows: iterable of (date_str, price) — date_str в формате 'YYYY-MM-DD'.
    Возвращает list[float] длинной ≤ max_points за последние `days` дней
    от самой свежей даты в rows. Равномерное сэмплирование, сортировка asc.
    Пустой ввод → [].
    """
    parsed = []
    for date_str, price in rows:
        d = _parse_date(date_str)
        if d is None:
            continue
        try:
            p = float(price)
        except (TypeError, ValueError):
            continue
        if p <= 0 or p >= 1000:  # фильтр мусора, как в dump_data_json.normalize_price
            continue
        parsed.append((d, p))
    if not parsed:
        return []

    parsed.sort(key=lambda x: x[0])
    latest = parsed[-1][0]
    cutoff = latest - timedelta(days=days)
    window = [(d, p) for d, p in parsed if d >= cutoff]
    if not window:
        return []

    if len(window) <= max_points:
        return [p for _, p in window]

    # Равномерное сэмплирование: берём индексы 0, step, 2*step, ..., последний
    step = (len(window) - 1) / (max_points - 1)
    sampled = []
    for i in range(max_points):
        idx = int(round(i * step))
        sampled.append(window[idx][1])
    return sampled


def build_history(region, prices_rows, limits_rows):
    """Собирает объект истории региона для /static/history/<region>.json.

    prices_rows: iterable of (date_str, price).
    limits_rows: iterable of (date_str, network, old_value, new_value).
    Возвращает dict с prices (asc, за 90 дней) и limits (desc).
    """
    parsed_prices = []
    for date_str, price in prices_rows:
        d = _parse_date(date_str)
        if d is None:
            continue
        try:
            p = float(price)
        except (TypeError, ValueError):
            continue
        if p <= 0 or p >= 1000:
            continue
        parsed_prices.append((d, p))
    parsed_prices.sort(key=lambda x: x[0])
    if parsed_prices:
        cutoff = parsed_prices[-1][0] - timedelta(days=90)
        parsed_prices = [(d, p) for d, p in parsed_prices if d >= cutoff]
    prices = [{"date": d.isoformat(), "price": p} for d, p in parsed_prices]

    parsed_limits = []
    for date_str, network, old_value, new_value in limits_rows:
        d = _parse_date(date_str)
        if d is None:
            continue
        parsed_limits.append((d, network or "все сети", old_value, new_value))
    parsed_limits.sort(key=lambda x: x[0], reverse=True)
    limits = [
        {"date": d.isoformat(), "network": net, "old": old_v, "new": new_v}
        for d, net, old_v, new_v in parsed_limits
    ]

    return {"region": region, "prices": prices, "limits": limits}
