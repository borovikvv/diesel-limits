import sqlite3
db = sqlite3.connect('/root/diesel_limits/restrictions.db')

# Ограничения по дизелю (август 2026)
restrictions = [
    ("г. Москва", None, "Газпромнефть", "физлица", "объем", "60 л дизель город, 200 л трасса", "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-08-12"),
    ("г. Москва", None, "Лукойл", "физлица", "объем", "20-30 л на клиента", "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-08-12"),
    ("Омская область", None, None, "все", "объем", "200 л дизель трасса, 80 л город (отменены 28 июля)", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-28"),
    ("Вологодская область", None, "Лукойл", "физлица", "объем", "200 л дизель трасса, 60 л город", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-08-12"),
    ("Мурманская область", None, "Лукойл", "физлица", "объем", "60 л дизель", "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-08-12"),
    ("Мурманская область", None, "Роснефть", "физлица", "объем", "без ограничений", "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-08-12"),
    ("Мурманская область", None, "Газпромнефть", "физлица", "объем", "30 л дизель, 60 л по карте лояльности", "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-08-12"),
    ("Самарская область", None, None, "физлица", "объем", "100 л дизель легковые", "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-08-12"),
    ("Пензенская область", None, None, "физлица", "объем", "200 л дизель, только в бак", "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-08-12"),
    ("Белгородская область", None, "Лукойл", "физлица", "объем", "60 л дизель", "https://www.rbc.ru/economics/03/07/2026/6a461d589a79474020d03021", "2026-07-03"),
    ("Белгородская область", None, "Роснефть", "физлица", "запрет", "запрет заправки в канистры", "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-08-12"),
    ("Ульяновская область", None, None, "физлица", "объем", "100 л дизель легковые, 300 л грузовые", "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-08-12"),
    ("Якутия", None, "Саханефтегазсбыт", "все", "объем", "200 л дизель, запрет в переносную тару", "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-08-12"),
    ("Республика Алтай", None, None, "все", "объем", "50-100 л дизель в сутки (50 л Чойский/Турочакский/Горно-Алтайск/Майма/Чемал, 100 л остальные)", "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-08-12"),
    ("Томская область", None, None, "все", "объем", "80 л дизель (Колпашевский, Асиновский, Зырянский, Тегульдетский р-ны)", "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-08-12"),
    ("Краснодарский край", None, None, "все", "объем", "30-60 л дизель на разных АЗС", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Приморский край", None, None, "грузовики", "объем", "100 л дизель город, 200 л трасса", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Кировская область", None, "Движение", "все", "объем", "100 л дизель", "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhi-benzina-69216288/", "2026-07-28"),
    ("Кемеровская область - Кузбасс", None, "Газпромнефть", "все", "объем", "80 л дизель, 200 л трасса", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-06-23"),
    ("Новосибирская область", None, None, "все", "объем", "60 л дизель", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-21"),
    ("Республика Татарстан", None, "Татнефть", "все", "объем", "60 л дизель легковые, 300 л грузовые, по топливным картам без лимита", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-08-12"),
    ("Тюменская область", None, "Газпромнефть", "все", "объем", "200 л дизель трасса, 80 л город", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-08-12"),
    ("Челябинская область", None, "Татнефть", "все", "объем", "60 л дизель", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-08-12"),
    ("Чувашская Республика - Чувашия", None, None, "грузовики", "объем", "300 л дизель", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-08-12"),
    ("Республика Карелия", None, None, "все", "объем", "60 л дизель, 250 л для большегрузов", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-08-12"),
    ("Калининградская область", None, None, "все", "объем", "60 л дизель", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-06-25"),
    ("Республика Дагестан", None, None, "физлица", "объем", "50 л дизель", "https://www.aa.com.tr/ru/экономика/география-ограничений-на-продажу-топлива-в-россии-продолжает-расширяться/3983182", "2026-07-01"),
    ("Воронежская область", None, "Лукойл", "все", "объем", "200 л дизель трасса, 60 л город", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-08-12"),
    ("Ивановская область", None, None, "все", "объем", "60-200 л дизель, только в бак", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-02"),
    ("Магаданская область", None, None, "все", "объем", "500 л дизель Магадан, 250 л остальные (до сентября)", "https://prim.rbc.ru/prim/13/07/2026/6a5456e09a7947c742a14001", "2026-07-13"),
    ("г. Севастополь", None, None, "все", "объем", "дизель в свободной продаже", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-07-04"),
    ("Республика Крым", None, None, "спецслужбы", "запрет", "заправка только спецслужбам", "https://finance.mail.ru/article/gde-v-rossii-ogranichili-prodazhu-benzina-69216968/", "2026-08-12"),
    ("Ямало-Ненецкий автономный округ", None, None, "все", "запрет", "запрет на отпуск топлива в тару", "https://www.sravni.ru/novost/2026/7/28/gde-vveli-ogranicheniya-na-benzin-v-iyune-2026-goda-regiony-i-limity/", "2026-08-12"),
    ("г. Санкт-Петербург", None, "Татнефть", "все", "объем", "40 л дизель", "https://www.rbc.ru/spb_sz/14/06/2026/6a2ecf3e9a794709c2039339", "2026-06-14"),
    ("Россия", None, None, "экспорт", "запрет", "запрет на экспорт дизельного топлива (до 31 июля, продлён)", "https://novayagazeta.ru/articles/2026/07/13/menshe-ezdit-budete", "2026-07-08"),
]

# Build existing index from DB
existing = {}
for row in db.execute("SELECT id, region, network, client_type, limit_type, limit_value, previous_value, is_current FROM restrictions"):
    key = (row[1], row[2] or '', row[3] or '', row[4] or '')
    existing[key] = row

count_new = 0
count_updated = 0

for r in restrictions:
    region, city, network, client_type, limit_type, limit_value, source_url, source_date = r
    key = (region, network or '', client_type or '', limit_type or '')
    
    if key in existing:
        rid, _, _, _, _, old_val, old_prev, old_current = existing[key]
        if old_val != limit_value:
            # UPDATE in place, preserve previous_value
            db.execute(
                "UPDATE restrictions SET limit_value=?, previous_value=?, source_url=?, source_date=?, is_current=1, updated_at=datetime('now') WHERE id=?",
                (limit_value, old_val, source_url, source_date, rid)
            )
            existing[key] = (rid, region, network, client_type, limit_type, limit_value, old_val, 1)
            count_updated += 1
    else:
        db.execute(
            "INSERT INTO restrictions(region,city,network,client_type,limit_type,limit_value,source_url,source_date,is_current) VALUES(?,?,?,?,?,?,?,?,1)",
            (region, city, network, client_type, limit_type, limit_value, source_url, source_date)
        )
        new_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        existing[key] = (new_id, region, network, client_type, limit_type, limit_value, None, 1)
        count_new += 1

db.commit()
print(f"Новых ограничений: {count_new}, обновлённых: {count_updated}")
db.close()
