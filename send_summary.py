#!/usr/bin/env python3
"""Send summary message to Telegram channel."""
import os, requests, sys

token = os.environ.get('TG_BOT_TOKEN_DIESEL', '')
if not token:
    print("ERROR: TG_BOT_TOKEN_DIESEL not set")
    sys.exit(1)

chat_id = "-1004299364641"

text = """<b>Что изменилось за сутки (28.07.2026):</b>

<b>Ограничения — обновлено 48 записей:</b>

Уточнены формулировки лимитов в большинстве регионов. Ключевые правки:
• Липецкая область — лимит 30 л бензина продлён до 1 августа
• Кировская область — лимит увеличен с 30 до 100 л (по номерам)
• Республика Калмыкия — конкретизирован лимит: до 30 л бензина
• Псковская область — фокус на дизель: до 40 л
• Нижегородская область — тест QR-кодов, заправка по дням
• Москва, Газпромнефть — добавлен лимит на бензин: 30 л + 60 л дизеля
• Москва, Лукойл — уточнено: 20-30 л топлива на клиента

<b>Цены — обновлены по всем 86 регионам:</b>
Средняя по РФ: 91,21 руб/л (данные Росстата на 13.07.2026)"""

resp = requests.post(
    f"https://api.telegram.org/bot{token}/sendMessage",
    data={"chat_id": chat_id, "parse_mode": "HTML", "text": text}
)
print(resp.status_code, resp.text)
