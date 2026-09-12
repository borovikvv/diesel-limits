#!/usr/bin/env python3
"""Send daily changes summary to Telegram + save to /srv/static/changelog_latest.txt."""
import os, sys, datetime, sqlite3, requests

token = os.environ.get('TG_BOT_TOKEN_DIESEL', '')
if not token:
    sys.exit("TG_BOT_TOKEN_DIESEL not set")

chat_id = '@disel_limits_update'
now_str = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
today = datetime.datetime.now().strftime('%d.%m.%Y')

db = sqlite3.connect('/root/diesel_limits/restrictions.db')

# Изменённые за сутки
cur = db.execute("""
    SELECT region, network, previous_value, limit_value, limit_type, updated_at
    FROM restrictions
    WHERE updated_at >= datetime('now', '-1 day')
    AND previous_value IS NOT NULL AND previous_value != ''
    ORDER BY region, network
""")
changes = cur.fetchall()

# Цены обновлённые
prices_cnt = db.execute(
    "SELECT COUNT(*) FROM prices WHERE updated_at >= datetime('now', '-1 day')"
).fetchone()[0]

# Средние цены
p_avg = db.execute("SELECT ROUND(AVG(price),1) FROM prices").fetchone()[0] or 0
p_min = db.execute("SELECT MIN(price) FROM prices").fetchone()[0] or 0
p_max = db.execute("SELECT MAX(price) FROM prices").fetchone()[0] or 0
db.close()

# Формируем summary
lines = []
lines.append(f"Что изменилось за сутки ({today}):")
lines.append("")

if changes:
    lines.append(f"Изменены ограничения ({len(changes)} записей):")
    lines.append("")
    for region, network, prev, new, ltype, ts in changes:
        net_str = f" ({network})" if network and network != "None" else ""
        lines.append(f"  {region}{net_str}: {prev} -> {new}")
    lines.append("")

if prices_cnt:
    lines.append(f"Обновлены цены в {prices_cnt} регионах.")
    lines.append(f"Средняя цена дизеля по РФ: {p_avg} руб/л (от {p_min} до {p_max}).")
    lines.append("")

lines.append("Данные: Росстат и сети АЗС.")

summary = "\n".join(lines)

# Отправка в Telegram
url = f'https://api.telegram.org/bot{token}/sendMessage'
resp = requests.post(url, data={
    'chat_id': chat_id,
    'text': summary,
}, timeout=60)
print(f"Summary: {resp.status_code}")
print(resp.text[:500])

# Сохранение для сайта
with open('/srv/static/changelog_latest.txt', 'w', encoding='utf-8') as f:
    f.write(summary + '\n')
    f.write(now_str + '\n')
print("Saved to /srv/static/changelog_latest.txt")
