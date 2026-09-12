import sqlite3
from datetime import date

db = sqlite3.connect('/root/diesel_limits/restrictions.db')
today = date.today().isoformat()

for r in db.execute('SELECT region, price FROM prices WHERE price IS NOT NULL'):
    db.execute('INSERT OR IGNORE INTO prices_history(region,date,price) VALUES(?,?,?)', 
               (r[0], today, float(r[1])))

db.commit()
print(f"Inserted prices_history for {today}")
db.close()
