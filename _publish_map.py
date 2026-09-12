#!/usr/bin/env python3
"""Publish diesel map to Telegram. Ponytail: minimal."""
import os, sys, datetime, sqlite3, requests
from PIL import Image

token = os.environ.get('TG_BOT_TOKEN_DIESEL', '')
if not token:
    sys.exit("TG_BOT_TOKEN_DIESEL not set")

chat_id = '@disel_limits_update'
now_str = datetime.datetime.now().strftime('%d.%m.%Y')

# Resize for Telegram
img = Image.open('/srv/static/diesel.png')
img.thumbnail((1280, 1280), Image.LANCZOS)
img.save('/tmp/diesel_tg.png', 'PNG')
print(f"Resized: {img.size}")

# Stats from DB
db = sqlite3.connect('/root/diesel_limits/restrictions.db')
p_cnt = db.execute("SELECT COUNT(*) FROM prices").fetchone()[0]
p_avg = db.execute("SELECT ROUND(AVG(price),1) FROM prices").fetchone()[0] or 0
p_min = db.execute("SELECT MIN(price) FROM prices").fetchone()[0] or 0
p_max = db.execute("SELECT MAX(price) FROM prices").fetchone()[0] or 0
r_active = db.execute("SELECT COUNT(*) FROM restrictions WHERE is_current=1").fetchone()[0]
r_changes = db.execute(
    "SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL "
    "AND updated_at >= datetime('now','-1 day')"
).fetchone()[0]
r_regions = db.execute(
    "SELECT COUNT(DISTINCT region) FROM restrictions WHERE is_current=1"
).fetchone()[0]
db.close()

caption = (
    f"Дизель-лимиты на {now_str}\n"
    f"Цены: {p_cnt} регионов, средняя {p_avg} руб/л ({p_min}-{p_max})\n"
    f"Ограничения: {r_active} записей в {r_regions} регионах"
)
if r_changes:
    caption += f"\nИзменений за сутки: {r_changes}"

url = f'https://api.telegram.org/bot{token}/sendPhoto'
with open('/tmp/diesel_tg.png', 'rb') as f:
    resp = requests.post(
        url,
        data={'chat_id': chat_id, 'caption': caption},
        files={'photo': ('diesel.png', f, 'image/png')},
        timeout=60
    )

print(f"Карта: {resp.status_code}")
print(resp.text[:500])
