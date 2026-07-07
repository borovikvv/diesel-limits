import sys, os, json, sqlite3, urllib.parse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import dump_history


SCHEMA = """
CREATE TABLE prices_history (region TEXT, price REAL, date TEXT);
CREATE TABLE restrictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region TEXT, city TEXT, network TEXT, client_type TEXT,
    limit_type TEXT, limit_value TEXT, source_url TEXT, source_date TEXT,
    is_current INTEGER, previous_value TEXT, updated_at TEXT
);
"""


def make_db():
    db = sqlite3.connect(":memory:")
    db.executescript(SCHEMA)
    return db


def test_collect_history_returns_region_data():
    db = make_db()
    db.executemany(
        "INSERT INTO prices_history(region,price,date) VALUES(?,?,?)",
        [("Москва", 60.0, "2026-06-01"), ("Москва", 62.0, "2026-06-10")],
    )
    db.executemany(
        "INSERT INTO restrictions(region,network,source_date,limit_value,previous_value,is_current) "
        "VALUES(?,?,?,?,?,?)",
        [("Москва", "Газпромнефть", "2026-06-05", "60 л", "100 л", 1)],
    )
    out = dump_history.collect_for_region(db, "Москва")
    assert out["region"] == "Москва"
    assert out["prices"] == [
        {"date": "2026-06-01", "price": 60.0},
        {"date": "2026-06-10", "price": 62.0},
    ]
    assert out["limits"] == [
        {"date": "2026-06-05", "network": "Газпромнефть", "old": "100 л", "new": "60 л"},
    ]


def test_collect_history_empty_region():
    db = make_db()
    out = dump_history.collect_for_region(db, "Чукотский АО")
    assert out == {"region": "Чукотский АО", "prices": [], "limits": []}


def test_write_history_files_creates_one_per_region(tmp_path):
    db = make_db()
    db.executemany(
        "INSERT INTO prices_history(region,price,date) VALUES(?,?,?)",
        [("Москва", 60.0, "2026-06-01")],
    )
    db.execute(
        "INSERT INTO restrictions(region,network,source_date,limit_value,is_current) "
        "VALUES('Москва','Лукойл','2026-06-01','40 л',1)"
    )
    out_dir = tmp_path / "history"
    dump_history.write_all(db, str(out_dir))
    files = list(out_dir.iterdir())
    assert len(files) == 1
    # имя файла = URL-encoded регион
    expected_name = urllib.parse.quote("Москва", safe="") + ".json"
    assert files[0].name == expected_name
    data = json.loads(files[0].read_text(encoding="utf-8"))
    assert data["region"] == "Москва"
    assert len(data["prices"]) == 1
