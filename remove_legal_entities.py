#!/usr/bin/env python3
"""Remove legal entity (juridicheskie litsa) restrictions from database."""
import sqlite3

db = sqlite3.connect('/root/diesel_limits/restrictions.db')

# List of client_type values to exclude
exclude_types = [
    'юридические лица',
    'юрлица',
    'юрлиц',
    'legal',
    'юридические',
    'юрлица/грузовики',
]

# Also exclude rows where client_type contains 'юр' but not 'физ'
# and rows containing 'ИП'

q = db.execute("SELECT id, client_type FROM restrictions")
to_delete = []
for row in q.fetchall():
    rid, ct = row
    if ct is None:
        continue
    ct_lower = ct.lower()
    if ct in exclude_types:
        to_delete.append(rid)
    elif 'юр' in ct_lower and 'физ' not in ct_lower:
        to_delete.append(rid)
    elif 'ип' in ct_lower and 'физ' not in ct_lower:
        to_delete.append(rid)

print(f'Found {len(to_delete)} rows to delete')

if to_delete:
    placeholders = ','.join('?' * len(to_delete))
    db.execute(f'DELETE FROM restrictions WHERE id IN ({placeholders})', to_delete)
    db.commit()

print(f'Active restrictions now: {db.execute("SELECT COUNT(*) FROM restrictions WHERE is_current=1").fetchone()[0]}')
print(f'Total restrictions now: {db.execute("SELECT COUNT(*) FROM restrictions").fetchone()[0]}')
db.close()
