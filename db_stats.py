#!/usr/bin/env python3
import sqlite3, os
db = sqlite3.connect('/root/diesel_limits/restrictions.db')
prices_count = db.execute('SELECT COUNT(*) FROM prices').fetchone()[0]
prices_with_value = db.execute('SELECT COUNT(*) FROM prices WHERE price IS NOT NULL').fetchone()[0]
active_restrictions = db.execute('SELECT COUNT(*) FROM restrictions WHERE is_current=1').fetchone()[0]
total_restrictions = db.execute('SELECT COUNT(*) FROM restrictions').fetchone()[0]
changes = db.execute('SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL').fetchone()[0]
history_count = db.execute('SELECT COUNT(*) FROM prices_history').fetchone()[0]
history_files = len(os.listdir('/srv/static/history'))
db.close()
print(f'prices: {prices_count} ({prices_with_value} с ценами)')
print(f'prices_history: {history_count} записей')
print(f'active restrictions: {active_restrictions}')
print(f'total restrictions: {total_restrictions}')
print(f'changes: {changes}')
print(f'history files: {history_files}')
