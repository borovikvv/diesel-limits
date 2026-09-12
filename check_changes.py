#!/usr/bin/env python3
import sqlite3, datetime

db = '/root/diesel_limits/restrictions.db'
con = sqlite3.connect(db)
con.row_factory = sqlite3.Row
cur = con.cursor()

# Изменённые записи (previous_value IS NOT NULL = было изменение)
cur.execute("SELECT COUNT(*) as cnt FROM restrictions WHERE updated_at >= datetime('now', '-1 day') AND previous_value IS NOT NULL")
r = cur.fetchone()
changed = r['cnt']
print(f'CHANGED:{changed}')

# Новые записи
cur.execute("SELECT COUNT(*) as cnt FROM restrictions WHERE updated_at >= datetime('now', '-1 day') AND previous_value IS NULL")
r = cur.fetchone()
new_records = r['cnt']
print(f'NEW:{new_records}')

# Детали изменений
cur.execute("SELECT * FROM restrictions WHERE updated_at >= datetime('now', '-1 day') ORDER BY updated_at")
rows = cur.fetchall()
print(f'TOTAL:{len(rows)}')
for r in rows:
    pv = r['previous_value'] if r['previous_value'] else ''
    print(f"ROW|{r['region']}|{r['network']}|{r['city']}|{r['limit_type']}|{r['limit_value']}|{pv}|{r['updated_at']}")

# Цены
cur.execute("SELECT COUNT(*) as cnt FROM prices WHERE updated_at >= datetime('now', '-1 day')")
r = cur.fetchone()
print(f'PRICES_CHANGED:{r["cnt"]}')

cur.execute("SELECT * FROM prices WHERE updated_at >= datetime('now', '-1 day') ORDER BY updated_at")
prices = cur.fetchall()
for p in prices:
    print(f"PRICE|{p['region']}|{p['price']}|{p['source_date']}|{p['updated_at']}")

con.close()
