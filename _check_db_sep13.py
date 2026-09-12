import sqlite3
db = sqlite3.connect('/root/diesel_limits/restrictions.db')

print("=== Schema restrictions ===")
for r in db.execute("PRAGMA table_info(restrictions)"):
    print(r)

print("\n=== Active restrictions ===")
rows = db.execute("SELECT * FROM restrictions WHERE is_current=1 ORDER BY region LIMIT 10").fetchall()
cols = [d[0] for d in db.execute("SELECT * FROM restrictions LIMIT 1").description]
print(f"Cols: {cols}")
active = db.execute("SELECT COUNT(*) FROM restrictions WHERE is_current=1").fetchone()[0]
print(f"Total active: {active}")
for r in rows:
    print(r)

total = db.execute("SELECT COUNT(*) FROM restrictions").fetchone()[0]
print(f"\nTotal: {total}")
changes = db.execute("SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL").fetchone()[0]
print(f"With changes: {changes}")

db.close()
