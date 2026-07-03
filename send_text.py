#!/usr/bin/env python3
"""Send text message to @disel_limits_update. Usage: python3 send_text.py "message" """
import requests, re, sys

with open("/root/diesel_limits/publish_diesel_map.py") as f:
    src = f.read()
bot = re.search(r'^BOT\s*=\s*"([^"]+)"', src, re.M).group(1)
chat = re.search(r'^CHAT\s*=\s*"([^"]+)"', src, re.M).group(1)

text = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read().strip()
r = requests.post(f"https://api.telegram.org/bot{bot}/sendMessage",
                  data={"chat_id": chat, "text": text, "parse_mode": "HTML"})
r.raise_for_status()
print("msg", r.json()["result"]["message_id"])
