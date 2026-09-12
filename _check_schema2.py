import sqlite3
db = sqlite3.connect('/root/diesel_limits/restrictions.db')
for row in db.execute("SELECT sql FROM sqlite_master WHERE name='restrictions'"):
    print(row[0])
print()
for row in db.execute("PRAGMA table_info(restrictions)"):
    print(row)
