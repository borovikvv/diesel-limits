#!/usr/bin/env python3
"""Dump restrictions + prices DB to /srv/static/data.json for the site."""
import sqlite3, json
from datetime import datetime

DB = "/root/diesel_limits/restrictions.db"
OUT = "/srv/static/data.json"

db = sqlite3.connect(DB)

prices = {}
for r in db.execute("SELECT region, price FROM prices"):
    prices[r[0]] = r[1]

restrictions = []
for r in db.execute("SELECT region, network, limit_value, client_type, source_url, source_date FROM restrictions WHERE is_current=1 ORDER BY source_date DESC, region"):
    restrictions.append({
        "region": r[0],
        "network": r[1],
        "limit": r[2],
        "client": r[3],
        "source": r[4],
        "date": r[5] or "—"
    })

data = {
    "prices": prices,
    "restrictions": restrictions,
    "updated": datetime.now().strftime("%d.%m.%Y %H:%M")
}

with open(OUT, "w") as f:
    json.dump(data, f, ensure_ascii=False)
import os; os.chmod(OUT, 0o644)

print(f"dumped {OUT}: {len(prices)} regions, {len(restrictions)} restrictions")
