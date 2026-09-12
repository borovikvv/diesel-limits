import sqlite3

db = sqlite3.connect('/root/diesel_limits/restrictions.db')
today = '2026-07-12'
source_main = 'https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/'
source_sravni = 'https://www.sravni.ru/novost/2026/7/9/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/'
source_mail = 'https://finance.mail.ru/article/gde-ogranichili-prodazhu-benzina-i-kogda-situaciya-normalizuetsya-69217153/'

new_restrictions = [
    ('Россия', '', 'Все', 'all', 'ban', 'Запрет на экспорт дизельного топлива (до 31 июля 2026)', 'https://ngs.ru/text/politics/2026/07/08/76523461/'),
    ('Россия', '', 'Все', 'all', 'ban', 'Разрешён оборот дизеля стандарта Евро-3 (сера до 350 мг/кг)', 'https://lenta.ru/news/2026/07/03/vrossii-razreshili-vypuskat-benzin-i-dizel-klassa-evro-3/'),
    ('Москва', 'Москва', 'Лукойл', 'physical', 'volume', '20-30 л бензина, дизель до 60 л, только в бак', source_main),
    ('Москва', 'Москва', 'Газпромнефть', 'physical', 'volume', '30 л бензина, 60 л дизеля (трасса 200 л дизеля)', source_main),
    ('Москва', 'Москва', 'Татнефть', 'physical', 'volume', '30 л АИ-95', source_main),
    ('Московская область', '', 'Лукойл', 'physical', 'volume', '20-30 л бензина, только в бак', source_main),
    ('Московская область', '', 'Газпромнефть', 'physical', 'volume', '30 л бензина, 60 л дизеля (трасса 200 л дизеля)', source_main),
    ('Санкт-Петербург', 'Санкт-Петербург', 'Все', 'physical', 'volume', '20-30 л бензина, 60 л дизеля; запрет канистры', source_main),
    ('Ленинградская область', '', 'Все', 'physical', 'volume', '20-30 л бензина, 60 л дизеля', source_main),
    ('Адыгея Республика', '', 'Все', 'physical', 'volume', 'Ограничен объём заправки легковых авто', source_main),
    ('Республика Алтай', 'Горно-Алтайск', 'Все', 'physical', 'volume', '30 л бензина, 50 л дизеля/сут (до 1 сен)', source_main),
    ('Республика Алтай', '', 'Все', 'physical', 'volume', '50 л бензина, 100 л дизеля/сут (остальные районы)', source_main),
    ('Архангельская область', '', 'Все', 'physical', 'volume', '20-50 л бензина', source_main),
    ('Башкортостан Республика', '', 'Все', 'physical', 'volume', '30 л бензина на авто, только в бак', source_main),
    ('Белгородская область', '', 'Лукойл', 'physical', 'volume', '30 л бензина, 60 л дизеля', source_main),
    ('Белгородская область', '', 'Роснефть', 'physical', 'ban', 'Запрещена заправка в канистры (кроме приграничных)', source_main),
    ('Брянская область', '', 'Все', 'physical', 'volume', 'Запрет продажи в канистры; до 20 л', source_main),
    ('Владимирская область', '', 'Все', 'physical', 'volume', '20-30 л бензина, 40 л дизеля; запрет канистры', source_main),
    ('Волгоградская область', '', 'Лукойл', 'physical', 'volume', 'Трассы: 60/200 л; город: 30/60 л', source_sravni),
    ('Вологодская область', '', 'Лукойл', 'physical', 'volume', '30/60 л (трассы: 30/200 л); только в бак', source_sravni),
    ('Воронежская область', '', 'Лукойл', 'physical', 'volume', '30/60 л (трассы: 60/200 л)', source_mail),
    ('Дагестан Республика', '', 'Все', 'physical', 'volume', '20 л бензина, 50 л дизеля', source_main),
    ('Забайкальский край', '', 'Все', 'physical', 'volume', '15 л бензина, только в бак', source_main),
    ('Ивановская область', '', 'Все', 'physical', 'volume', '30/60 л; только в бак', source_sravni),
    ('Иркутская область', '', 'Роснефть', 'physical', 'volume', 'До 50 л/сут на авто', source_mail),
    ('Калининградская область', '', 'Все', 'physical', 'volume', '30/60 л в один бак', source_main),
    ('Карелия Республика', '', 'Лукойл', 'physical', 'volume', '30/60 л (большегрузы 250 л); мин 10 л', source_sravni),
    ('Кемеровская область', '', 'Газпромнефть', 'physical', 'volume', '40/80 л (трассы: 40/200 л)', source_sravni),
    ('Краснодарский край', '', 'Все', 'physical', 'volume', '20-30/30-60 л; запрет канистры', source_main),
    ('Красноярский край', '', 'Газпромнефть', 'physical', 'volume', '20-40/40-80 л (трасса 200 л); запрет канистры', source_main),
    ('Республика Крым', '', 'Все', 'all', 'ban', 'Полное ограничение продажи; топливо только госслужбам', source_main),
    ('Севастополь', 'Севастополь', 'Все', 'all', 'ban', 'Полное ограничение свободной продажи', source_main),
    ('Курганская область', '', 'Все', 'physical', 'volume', 'Трассы: 40/200 л; город: 40/80 л', source_sravni),
    ('Липецкая область', '', 'Все', 'physical', 'volume', '30 л бензина; по чётным/нечётным номерам', source_sravni),
    ('Мордовия Республика', '', 'Все', 'physical', 'volume', '20/60 л (легк), 300 л (груз); по номерам', source_sravni),
    ('Мурманская область', '', 'Лукойл', 'physical', 'volume', '30/60 л', source_mail),
    ('Мурманская область', '', 'Роснефть', 'physical', 'volume', '99 л бензина, дизель без ограничений', source_mail),
    ('Мурманская область', '', 'Газпромнефть', 'physical', 'volume', '30/30 л (карта: 60 л дизеля)', source_mail),
    ('Нижегородская область', '', 'Все', 'physical', 'volume', 'До 40 л бензина; по чётным/нечётным', source_sravni),
    ('Новосибирская область', '', 'Все', 'physical', 'volume', '30/60 л', source_sravni),
    ('Омская область', '', 'Все', 'physical', 'volume', '40/80 л (трассы: 40/200 л)', source_mail),
    ('Орловская область', '', 'Все', 'physical', 'volume', '30-50 л бензина; по госномеру', source_mail),
    ('Пензенская область', '', 'Все', 'physical', 'volume', '100/200 л; только в бак', source_sravni),
    ('Приморский край', '', 'Все', 'physical', 'volume', 'Только в бак; груз: 100 л, трассы: 200 л', source_sravni),
    ('Ростовская область', '', 'Все', 'physical', 'volume', '30/60 л (легк); 200 л (груз); 300 л (автобусы)', source_sravni),
    ('Самарская область', '', 'Все', 'physical', 'volume', '40/100 л; запрет канистры', source_mail),
    ('Саратовская область', '', 'Все', 'physical', 'volume', '30 л бензина (до 15 июля)', source_mail),
    ('Свердловская область', 'Екатеринбург', 'Газпромнефть', 'physical', 'volume', '40 л бензина и дизеля', source_sravni),
    ('Республика Татарстан', '', 'Татнефть', 'physical', 'volume', '30 л АИ-95', source_sravni),
    ('Республика Татарстан', '', 'Газпромнефть', 'physical', 'volume', '30/60 л', source_mail),
    ('Тюменская область', '', 'Газпромнефть', 'physical', 'volume', '40/80 л (трассы: 40/200 л)', source_sravni),
    ('Ульяновская область', '', 'Все', 'physical', 'volume', '40/100 л (легк); 300 л (груз/автобусы)', source_sravni),
    ('Ханты-Мансийский автономный округ', '', 'Газпромнефть', 'physical', 'volume', '40/80 л', source_mail),
    ('Республика Саха (Якутия)', '', 'Саханефтегазсбыт', 'physical', 'volume', '30/200 л; запрет в тару', source_sravni),
    ('Астраханская область', '', 'Все', 'physical', 'time', 'По чётным/нечётным номерам', source_mail),
    ('Псковская область', '', 'Сургутнефтегаз', 'physical', 'time', 'АИ-92 с 14:00; АИ-95 круглосуточно; по номерам', source_mail),
    ('Ямало-Ненецкий автономный округ', '', 'Все', 'physical', 'volume', 'Запрет в тару; 40-70 л на машину', source_sravni),
    ('Чувашская Республика', '', 'Все', 'physical', 'ban', 'Запрет отпуска топлива в канистры', source_mail),
    ('Смоленская область', '', 'Все', 'physical', 'volume', '30/60 л (юрлица 300 л дизеля)', source_sravni),
    ('Томская область', '', 'Все', 'physical', 'volume', '30-40/80 л', source_mail),
]

# Use INSERT OR REPLACE with the unique constraint
c = db.cursor()
new_count = 0
for r in new_restrictions:
    region, city, network, client_type, limit_type, limit_value, url = r
    try:
        c.execute(
            'INSERT OR REPLACE INTO restrictions(region,city,network,client_type,limit_type,limit_value,source_url,source_date,is_current,updated_at) VALUES(?,?,?,?,?,?,?,?,1,datetime("now"))',
            (region, city, network, client_type, limit_type, limit_value, url, today)
        )
        new_count += 1
    except Exception as e:
        print(f"Error: {e} for {region}/{network}/{client_type}/{limit_type}")

db.commit()
print(f"Inserted/updated: {new_count}")
print(f"Total: {c.execute('SELECT COUNT(*) FROM restrictions').fetchone()[0]}")
print(f"Active: {c.execute('SELECT COUNT(*) FROM restrictions WHERE is_current=1').fetchone()[0]}")
print(f"Changes: {c.execute('SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL').fetchone()[0]}")
db.close()
