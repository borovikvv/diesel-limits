import sqlite3
db = sqlite3.connect('/root/diesel_limits/restrictions.db')
for row in db.execute('SELECT sql FROM sqlite_master'):
    print(row[0])
print('---prices count---')
print(db.execute('SELECT COUNT(*) FROM prices').fetchone())
print('---restrictions count---')
print(db.execute('SELECT COUNT(*) FROM restrictions').fetchone())
print('---prices sample---')
for r in db.execute('SELECT * FROM prices LIMIT 3').fetchall():
    print(r)
print('---restrictions sample---')
for r in db.execute('SELECT * FROM restrictions LIMIT 3').fetchall():
    print(r)
db.close()
