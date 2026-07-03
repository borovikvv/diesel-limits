#!/usr/bin/env python3
"""Send text message to @disel_limits_update.

Usage: python3 send_text.py "message"
       echo "message" | python3 send_text.py

Улучшения:
- Токен берётся из TG_BOT_TOKEN (как и в publish_diesel_map.py), а не парсится
  регэкспом из соседнего файла (это был небезопасный хак).
- Понятная ошибка, если токен не задан.
"""
import os
import sys
import requests

BOT = os.environ.get("TG_BOT_TOKEN")
if not BOT:
    sys.exit("❌ TG_BOT_TOKEN не задан в окружении. "
             "export TG_BOT_TOKEN='ваш_токен'")

CHAT = os.environ.get("TG_CHAT_ID", "-1004299364641")

text = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read().strip()
if not text:
    sys.exit("❌ Не передано сообщение. Usage: send_text.py 'текст сообщения'")

r = requests.post(
    f"https://api.telegram.org/bot{BOT}/sendMessage",
    data={"chat_id": CHAT, "text": text, "parse_mode": "HTML"},
    timeout=10
)
r.raise_for_status()
print("msg", r.json()["result"]["message_id"])
