#!/usr/bin/env python3
"""Final check. Ponytail: one-shot."""
import sqlite3, os
db = sqlite3.connect('/root/diesel_limits/restrictions.db')
prices = db.execute('SELECT COUNT(*) FROM prices').fetchone()[0]
active = db.execute('SELECT COUNT(*) FROM restrictions WHERE is_current=1').fetchone()[0]
total = db.execute('SELECT COUNT(*) FROM restrictions').fetchone()[0]
changes = db.execute('SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL').fetchone()[0]
history = len(os.listdir('/srv/static/history'))
print(f'prices: {prices}, active restrictions: {active}, total restrictions: {total}, changes: {changes}, history files: {history}')
db.close()
