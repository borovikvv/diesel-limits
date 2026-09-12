#!/usr/bin/env python3
import sqlite3, os
db = sqlite3.connect('/root/diesel_limits/restrictions.db')
prices = db.execute('SELECT COUNT(*) FROM prices').fetchone()[0]
active = db.execute('SELECT COUNT(*) FROM restrictions WHERE is_current=1').fetchone()[0]
total = db.execute('SELECT COUNT(*) FROM restrictions').fetchone()[0]
changes = db.execute('SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL').fetchone()[0]
history_files = len(os.listdir('/srv/static/history'))
history_records = db.execute('SELECT COUNT(*) FROM prices_history').fetchone()[0]
regions_with_prices = db.execute('SELECT COUNT(DISTINCT region) FROM prices WHERE price IS NOT NULL').fetchone()[0]
print(f'prices: {prices}, regions_with_prices: {regions_with_prices}, active restrictions: {active}, total restrictions: {total}, changes: {changes}, history files: {history_files}, history records: {history_records}')
db.close()
