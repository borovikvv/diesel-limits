import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from spark import build_price_spark, build_history


def test_price_spark_empty():
    assert build_price_spark([]) == []


def test_price_spark_few_points_returned_all():
    # 3 точки — меньше max_points, вернуть все по порядку
    rows = [("2026-06-01", 60.0), ("2026-06-05", 61.0), ("2026-06-10", 62.0)]
    assert build_price_spark(rows) == [60.0, 61.0, 62.0]


def test_price_spark_downsamples_to_max_points():
    # 24 точки → сэмплировать до 12
    rows = [("2026-06-%02d" % (d+1), 60.0 + d) for d in range(24)]
    result = build_price_spark(rows, days=30, max_points=12)
    assert len(result) == 12
    # первая точка = минимальная цена (раньшая дата), последняя = последняя
    assert result[0] == 60.0
    assert result[-1] == 83.0  # 60 + 23


def test_price_spark_filters_last_30_days():
    # точки за 60 дней, но days=30 → только последние 30 дней учитываются
    rows = [("2026-05-01", 50.0), ("2026-06-25", 70.0)]
    # самая свежая дата = 2026-06-25, отсечка = 2026-05-26; 2026-05-01 отбрасывается
    result = build_price_spark(rows, days=30, max_points=12)
    assert result == [70.0]


def test_history_prices_sorted_asc_limits_desc():
    prices = [("2026-06-02", 61.0), ("2026-06-01", 60.0)]
    limits = [
        ("2026-06-01", "Газпромнефть", "100 л", "60 л"),
        ("2026-06-05", "Лукойл", None, "40 л"),
    ]
    h = build_history("Московская область", prices, limits)
    assert h["region"] == "Московская область"
    assert h["prices"] == [
        {"date": "2026-06-01", "price": 60.0},
        {"date": "2026-06-02", "price": 61.0},
    ]
    assert h["limits"] == [
        {"date": "2026-06-05", "network": "Лукойл", "old": None, "new": "40 л"},
        {"date": "2026-06-01", "network": "Газпромнефть", "old": "100 л", "new": "60 л"},
    ]


def test_history_empty_inputs():
    h = build_history("Чукотский АО", [], [])
    assert h == {"region": "Чукотский АО", "prices": [], "limits": []}
