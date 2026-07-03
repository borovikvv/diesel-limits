#!/usr/bin/env python3
"""Send diesel heatmap + daily changes summary to @disel_limits_update."""
import requests, sqlite3
from PIL import Image
from datetime import datetime

BOT = "8878746981:AAFERGgoO7ZWK_EjLV3zEVPZToG0c7GWItw"
CHAT = "-1004299364641"
DB = "/root/diesel_limits/restrictions.db"

today = datetime.now().strftime("%d.%m.%Y")
db = sqlite3.connect(DB)

# prices
p_cnt = db.execute("SELECT COUNT(*) FROM prices").fetchone()[0]
p_avg = db.execute("SELECT ROUND(AVG(price),1) FROM prices").fetchone()[0]
p_min = db.execute("SELECT MIN(price) FROM prices").fetchone()[0]
p_max = db.execute("SELECT MAX(price) FROM prices").fetchone()[0]

# restrictions active
r_active = db.execute("SELECT COUNT(*) FROM restrictions WHERE is_current=1").fetchone()[0]
r_changes = db.execute("SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL AND updated_at >= datetime('now','-1 day')").fetchone()[0]

# regions under restrictions (distinct)
r_regions = db.execute("SELECT COUNT(DISTINCT region) FROM restrictions WHERE is_current=1").fetchone()[0]

db.close()

caption = (
    f"♻ Дизель-лимиты • {today}\n"
    f"📊 Цены: {p_cnt} рег., средняя {p_avg} ₽/л ({p_min}-{p_max})\n"
    f"⛔ Ограничения: {r_active} шт. в {r_regions} регионах"
)
if r_changes:
    caption += f"\n🔄 Изменений за сутки: {r_changes}"

# Resize to Telegram-safe dimensions (max 1280px wide)
img = Image.open("/srv/static/diesel.png")
img.thumbnail((1280, 1280), Image.LANCZOS)
img.save("/tmp/diesel_tg.png", "PNG")

url = f"https://api.telegram.org/bot{BOT}/sendPhoto"
with open("/tmp/diesel_tg.png", "rb") as f:
    r = requests.post(url, data={"chat_id": CHAT, "caption": caption}, files={"photo": f})
r.raise_for_status()
print("sent", r.json()["result"]["message_id"])
