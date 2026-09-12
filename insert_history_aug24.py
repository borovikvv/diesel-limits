#!/usr/bin/env python3
"""Insert prices_history for today."""
import sqlite3
from datetime import datetime

db = sqlite3.connect('/root/diesel_limits/restrictions.db')
today = datetime.now().strftime('%Y-%m-%d')

for r in db.execute('SELECT region, price FROM prices WHERE price IS NOT NULL'):
    db.execute('INSERT OR REPLACE INTO prices_history(region,date,price) VALUES(?,?,?)', 
               (r[0], today, float(r[1])))

db.commit()
cnt = db.execute('SELECT COUNT(*) FROM prices_history').fetchone()[0]
print(f"History: {cnt} records")
db.close()
