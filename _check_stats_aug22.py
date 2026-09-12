import sqlite3
db = sqlite3.connect('/root/diesel_limits/restrictions.db')
print(f'prices: {db.execute("SELECT COUNT(*) FROM prices").fetchone()[0]}')
print(f'active restrictions: {db.execute("SELECT COUNT(*) FROM restrictions WHERE is_current=1").fetchone()[0]}')
print(f'total restrictions: {db.execute("SELECT COUNT(*) FROM restrictions").fetchone()[0]}')
print(f'changes: {db.execute("SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL").fetchone()[0]}')
print(f'history: {db.execute("SELECT COUNT(*) FROM prices_history").fetchone()[0]}')
db.close()

import os
hist_files = len(os.listdir('/srv/static/history')) if os.path.exists('/srv/static/history') else 0
print(f'history files: {hist_files}')
