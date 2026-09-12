import sqlite3, os
db = sqlite3.connect('/root/diesel_limits/restrictions.db')
p = db.execute("SELECT COUNT(*) FROM prices WHERE price IS NOT NULL").fetchone()[0]
h = db.execute("SELECT COUNT(*) FROM prices_history").fetchone()[0]
active = db.execute("SELECT COUNT(*) FROM restrictions WHERE is_current=1").fetchone()[0]
total = db.execute("SELECT COUNT(*) FROM restrictions").fetchone()[0]
changes = db.execute("SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL").fetchone()[0]
hist_files = len(os.listdir("/srv/static/history"))
db.close()
print(f"prices: {p}, history: {h}, active restrictions: {active}, total restrictions: {total}, changes: {changes}, history files: {hist_files}")
