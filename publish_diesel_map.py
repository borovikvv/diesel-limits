#!/usr/bin/env python3
"""Send diesel heatmap to Telegram channel @disel_limits_update."""
import requests
from PIL import Image
BOT = "8878746981:AAFERGgoO7ZWK_EjLV3zEVPZToG0c7GWItw"
CHAT = "-1004299364641"
# Resize to Telegram-safe dimensions (max 1280px wide)
img = Image.open("/srv/static/diesel.png")
img.thumbnail((1280, 1280), Image.LANCZOS)
img.save("/tmp/diesel_tg.png", "PNG")
url = f"https://api.telegram.org/bot{BOT}/sendPhoto"
with open("/tmp/diesel_tg.png", "rb") as f:
    r = requests.post(url, data={"chat_id": CHAT, "caption": "♻ Карта обновлена на сегодня"}, files={"photo": f})
r.raise_for_status()
print("sent", r.json()["result"]["message_id"])
