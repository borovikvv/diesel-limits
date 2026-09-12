import sqlite3
db = sqlite3.connect('/root/diesel_limits/restrictions.db')
print('prices:', db.execute('SELECT COUNT(*) FROM prices').fetchone()[0])
print('current restrictions:', db.execute('SELECT COUNT(*) FROM restrictions WHERE is_current=1').fetchone()[0])
print('total restrictions:', db.execute('SELECT COUNT(*) FROM restrictions').fetchone()[0])
print('latest price update:', db.execute('SELECT MAX(updated_at) FROM prices').fetchone()[0])
print('---')
print('regions with prices:')
for r in db.execute('SELECT region, price FROM prices WHERE price IS NOT NULL ORDER BY region'):
    print(f'  {r[0]}: {r[1]}')
print('---')
print('active restrictions by region:')
for r in db.execute('SELECT DISTINCT region FROM restrictions WHERE is_current=1 ORDER BY region'):
    print(f'  {r[0]}')
db.close()
