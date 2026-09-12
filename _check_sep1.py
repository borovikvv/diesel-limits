import sqlite3, os
db = sqlite3.connect('/root/diesel_limits/restrictions.db')
print('PRICES:', db.execute('SELECT COUNT(*) FROM prices').fetchone()[0])
print('ACTIVE:', db.execute('SELECT COUNT(*) FROM restrictions WHERE is_current=1').fetchone()[0])
print('TOTAL:', db.execute('SELECT COUNT(*) FROM restrictions').fetchone()[0])
print('HISTORY:', db.execute('SELECT COUNT(*) FROM prices_history').fetchone()[0])
print('HISTORY_DIR:', len(os.listdir('/srv/static/history')))
for r in db.execute('SELECT region, price, source_date FROM prices LIMIT 5'):
    print('  SAMPLE:', r)
db.close()
