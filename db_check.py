import sqlite3
db = sqlite3.connect('/root/diesel_limits/restrictions.db')
print('=== PRICES (first 5) ===')
for row in db.execute('SELECT region, price, source_date FROM prices ORDER BY region LIMIT 5'):
    print(row)
print('=== RESTRICTIONS COUNT ===')
print('total:', db.execute('SELECT COUNT(*) FROM restrictions').fetchone()[0])
print('active:', db.execute('SELECT COUNT(*) FROM restrictions WHERE is_current=1').fetchone()[0])
print('=== HISTORY ===')
print('history:', db.execute('SELECT COUNT(*) FROM prices_history').fetchone()[0])
print('=== SCHEMA ===')
for row in db.execute("SELECT sql FROM sqlite_master WHERE type='table'"):
    print(row[0])
db.close()
