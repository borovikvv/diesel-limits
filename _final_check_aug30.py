#!/usr/bin/env python3
import sqlite3, os
db = sqlite3.connect('/root/diesel_limits/restrictions.db')
p = db.execute('SELECT COUNT(*) FROM prices').fetchone()[0]
a = db.execute('SELECT COUNT(*) FROM restrictions WHERE is_current=1').fetchone()[0]
t = db.execute('SELECT COUNT(*) FROM restrictions').fetchone()[0]
pv = db.execute('SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL').fetchone()[0]
h = db.execute('SELECT COUNT(*) FROM prices_history').fetchone()[0]
hf = len(os.listdir('/srv/static/history'))
print(f'prices: {p}')
print(f'active restrictions: {a}')
print(f'total restrictions: {t}')
print(f'changes (with previous_value): {pv}')
print(f'prices_history: {h}')
print(f'history files: {hf}')
print(f'diesel.png: {os.path.exists("/srv/static/diesel.png")}')
print(f'data.json: {os.path.exists("/srv/static/data.json")}')
db.close()
