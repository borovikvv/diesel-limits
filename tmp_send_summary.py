import os, datetime, urllib.request, urllib.error, json

token = os.environ.get('TG_BOT_TOKEN_DIESEL', '')
chat_id = '@disel_limits_update'

today = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')

summary = (
    "\U0001f4ca Обновление за " + today.split()[0] + "\n\n"
    "Добавлены новые ограничения в 16 регионах и обновлены цены по 84 регионам.\n\n"
    "Новые ограничения на дизель:\n\n"
    "\U0001f539 Краснодарский край — 30–60 л, разные АЗС\n"
    "\U0001f539 Приморский край — 100 л (город) / 200 л (трасса) для юрлиц\n"
    "\U0001f539 Псковская область — 40 л\n"
    "\U0001f539 Удмуртия — 40 л\n"
    "\U0001f539 Кировская область — до 100 л\n"
    "\U0001f539 Ульяновская область — до 100 л\n"
    "\U0001f539 Калининградская область — 60 л\n"
    "\U0001f539 Дагестан — 50 л\n"
    "\U0001f539 Курганская область — 80 л (город) / 200 л (трасса), только в бак\n"
    "\U0001f539 Омская область — 80 л (город) / 200 л (трасса), только в бак\n"
    "\U0001f539 Якутия — 200 л, только по топливным картам\n"
    "\U0001f539 Белгородская область — Лукойл, 60 л для физлиц\n"
    "\U0001f539 Ленинградская область / СПб — Лукойл, Газпромнефть, Teboil, 60 л\n"
    "\U0001f539 Самарская область — до 100 л\n"
    "\U0001f539 Республика Адыгея — ограничения действуют, точные лимиты не уточнены\n"
    "\U0001f539 Севастополь — дизель в свободной продаже, бензин по QR-кодам\n\n"
    "Цены обновлены по всем 84 регионам. Данные Росстата и сетей АЗС."
)

url = f'https://api.telegram.org/bot{token}/sendMessage'
payload = json.dumps({
    'chat_id': chat_id,
    'text': summary
}).encode('utf-8')

req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}, method='POST')
try:
    resp = urllib.request.urlopen(req, timeout=30)
    result = resp.read().decode()
    data = json.loads(result)
    print('SUMMARY SENT:', data.get('ok'))
    print('MSG_ID:', data.get('result', {}).get('message_id'))
except urllib.error.HTTPError as e:
    print('HTTP ERROR:', e.code, e.read().decode()[:500])
except Exception as e:
    print('ERROR:', str(e))
