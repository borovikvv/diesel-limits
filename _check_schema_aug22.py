import sqlite3
db = sqlite3.connect('/root/diesel_limits/restrictions.db')
for row in db.execute('PRAGMA table_info(restrictions)'):
    print(row)
db.close()
