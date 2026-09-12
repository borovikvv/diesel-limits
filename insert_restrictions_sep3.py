#!/usr/bin/env python3
import sqlite3

db = sqlite3.connect('/root/diesel_limits/restrictions.db')

# Свежие ограничения на ДТ (август-сентябрь 2026)
restrictions = [
    ('Республика Алтай',None,'все','все','объем','50 л бензина и 100 л дизеля, в канистры 10 л','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Оренбургская область',None,'все','все','объем','60 л дизеля в городе, 200 л на трассах','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Дагестан',None,'все','физлица','объем','20 л бензина и 50 л дизеля, только в бак','https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/','2026-08-19'),
    ('Калининградская область',None,'Лукойл, Сургутнефтегаз','все','отмена','без ограничений','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-07-28'),
    ('Калининградская область',None,'другие АЗС','все','объем','30 л бензина и 60-100 л дизеля','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Красноярский край',None,'некоторые АЗС','все','отмена','отменяют лимиты на дизель','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-13'),
    ('Хабаровский край',None,'независимые АЗС','все','отмена','снимают ограничения','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-25'),
    ('Иркутская область',None,'КрайсНефть','физлица','объем','30 л бензина, 20 л в канистры','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-13'),
    ('Липецкая область',None,'Газпром, Лукойл, Teboil, Роснефть','все','чет-нечет','четные/нечетные номера, дизель без ограничений','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-13'),
    ('Липецкая область',None,'все','все','объем','30 л бензина, дизель без ограничений','https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/','2026-08-19'),
    ('Владимирская область',None,'все','все','время','7:00-10:00 только экстренные службы','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Тверская область',None,'некоторые АЗС','все','время','5:30-7:30 только экстренные службы','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Крым и Севастополь',None,'все','все','объем','20 л бензина и 40 л дизеля, только в бак, бензин по QR','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Новосибирская область',None,'все','все','объем','30 л бензина и 60 л дизеля','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Новосибирская область',None,'все','все','запрет','запрещена продажа лицам младше 18 лет','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Пензенская область',None,'все','все','объем','100 л бензина и 200 л дизеля, в канистру 20 л','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Тамбовская область',None,'сетевые АЗС','все','объем','30 л бензина','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Томская область',None,'некоторые АЗС','все','объем','30-40 л бензина и 80 л дизеля','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Тюменская область',None,'Газпромнефть','все','объем','трассы: 40 л бензина и 200 л дизеля, город: 40 л бензина и 80 л дизеля','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Удмуртия',None,'все','все','объем','30-50 л бензина, 80-400 л дизеля','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Якутия',None,'все','все','объем','20-30 л бензина и 50-200 л дизеля, только по картам или в бак','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Белгородская область',None,'все','все','объем','30 л бензина и 60 л дизеля, запрет в канистры','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Волгоградская область',None,'Лукойл','все','объем','40 л бензина, 60 л дизеля город, 200 л трасса','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Ивановская область',None,'все','все','объем','30 л бензина и 60-200 л дизеля, только в бак','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Калмыкия',None,'все','все','объем','50 л бензина','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Карелия',None,'все','все','объем','40 л бензина и 60 л дизеля, для большегрузов 250 л дизеля','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Курганская область',None,'все','все','объем','трассы: 40 л бензина и 200 л дизеля, город: 40 л бензина и 80 л дизеля','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Магаданская область','Магадан','все','все','объем','500 л дизеля в Магадане, 250 л в области, 100 л бензина в сутки','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Мордовия',None,'все','все','объем','40 л бензина, 60 л дизеля легковые, 300 л грузовые','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Мурманская область',None,'Лукойл','все','объем','30 л бензина и 60 л дизеля','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Мурманская область',None,'Роснефть','все','объем','99 л бензина','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Мурманская область',None,'Газпромнефть','все','объем','30 л бензина и дизеля, по картам 60 л дизеля','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Ростовская область',None,'все','все','объем','30 л бензина и 60 л дизеля легковые, 200 л грузовики, 300 л автобусы','https://www.rbc.ru/economics/10/07/2026/6a50e9859a7947e50d76ffd8','2026-07-10'),
    ('Самарская область',None,'все','все','объем','40 л бензина и 100 л дизеля легковые, 300 л грузовики','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Смоленская область',None,'все','все','объем','30 л бензина и 60 л дизеля, только в бак','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Ульяновская область',None,'все','все','объем','40 л бензина, 100 л дизеля легковые, 300 л грузовики и автобусы','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Омская область',None,'все','все','объем','40 л бензина и 80 л дизеля, трассы: 200 л дизеля','https://www.rbc.ru/economics/22/06/2026/6a39803c9a7947ab8743ab42','2026-06-22'),
    ('Кемеровская область',None,'все','все','объем','40 л бензина и 80 л дизеля, трассы: 200 л дизеля','https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm','2026-08-19'),
    ('Краснодарский край',None,'все','все','объем','20-30 л бензина','https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/','2026-08-19'),
    ('Москва',None,'все','все','объем','20-30 л бензина и 60 л дизеля, трассы: 200 л дизеля','https://lenta.ru/twz/chto-proiskhodit/prodazha-topliva.htm','2026-08-19'),
    ('Воронежская область',None,'все','все','объем','30-40 л бензина и 60-200 л дизеля','https://lenta.ru/articles/2026/08/19/ogranicheniya-na-pokupku-benzina-v-rossii-v-avguste-2026-goda/','2026-08-19'),
    ('Башкортостан',None,'Татнефть','все','объем','50 л бензина АИ-92 и АИ-95, 400 л дизеля','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Псковская область',None,'сетевые АЗС','все','объем','30 л и более','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Челябинская область',None,'все','все','объем','20-30 л бензина','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
    ('Чувашия',None,'все','все','объем','20-40 л бензина','https://www.sravni.ru/novost/2026/8/25/v-rossii-snova-vvodyat-ogranicheniya-na-prodazhu-topliva-regiony-i-limity-v-avguste-2026-goda/','2026-08-26'),
]

for region, city, network, client_type, limit_type, value, url, date in restrictions:
    db.execute('''INSERT OR REPLACE INTO restrictions 
                  (region,city,network,client_type,limit_type,limit_value,source_url,source_date,is_current,updated_at) 
                  VALUES (?,?,?,?,?,?,?,?,1,datetime('now'))''',
               (region, city, network, client_type, limit_type, value, url, date))

db.commit()
db.close()
print(f'Сохранено {len(restrictions)} ограничений')
