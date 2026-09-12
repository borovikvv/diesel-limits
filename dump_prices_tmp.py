#!/usr/bin/env python3
"""Dump prices from DB for map gen."""
import sqlite3
db = sqlite3.connect('/root/diesel_limits/restrictions.db')
rows = db.execute('SELECT region, price FROM prices WHERE price IS NOT NULL ORDER BY region').fetchall()
for r,p in rows:
    print(f"{r}\t{p}")
db.close()
