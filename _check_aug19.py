import sqlite3, os
db = sqlite3.connect('/root/diesel_limits/restrictions.db')
prices = db.execute('SELECT COUNT(*) FROM prices WHERE price IS NOT NULL').fetchone()[0]
active_restr = db.execute('SELECT COUNT(*) FROM restrictions WHERE is_current=1').fetchone()[0]
total_restr = db.execute('SELECT COUNT(*) FROM restrictions').fetchone()[0]
with_prev = db.execute('SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL').fetchone()[0]
history_count = len(os.listdir('/srv/static/history')) if os.path.exists('/srv/static/history') else 0
history_rows = db.execute('SELECT COUNT(*) FROM prices_history').fetchone()[0]
print(f'prices: {prices}, active restrictions: {active_restr}, total restrictions: {total_restr}, changes: {with_prev}, history files: {history_count}, history rows: {history_rows}')
db.close()
