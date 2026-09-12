#!/usr/bin/env python3
"""Insert/refresh fresh restrictions based on sravni.ru Aug-26 data.
Schema: id, region, city, network, client_type, limit_type, limit_value,
        previous_value, source_url, source_date, is_current, created_at, updated_at
"""
import sqlite3
DB = "/root/diesel_limits/restrictions.db"

# (region, city, network, client_type, limit_type, limit_value, prev_value, source_url, source_date, is_current, note_for_city)
# limit_type maps to restriction category; we put note info into city when no city
fresh = [
    # Астраханская область: четные/нечетные номера, 30л АИ-92/95
    ("Астраханская область",None,None,"физлица","even_odd_plates",30,30,"https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/","2026-08-13",1),
    # Калужская область: четные/нечетные по началу номера, не на трассе, не на дизель
    ("Калужская область",None,None,"физлица","even_odd_plates_start",None,None,"https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/","2026-08-13",1),
    # Тамбовская область: 30л бензин, чет/нечет
    ("Тамбовская область",None,None,"физлица","volume_limit",30,30,"https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/","2026-08-13",1),
    # Ленинградская область: сняты дизель-лимиты
    ("Ленинградская область",None,None,"все","softened",None,None,"https://www.fontanka.ru/2026/08/05/76572500/","2026-08-05",1),
    # Новгородская область: запрет <18 с 01.09
    ("Новгородская область",None,None,"физлица","age_restriction",None,None,"https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/","2026-08-26",1),
    # Новосибирская область: 30л бензин, 60л дизель
    ("Новосибирская область",None,None,"физлица","volume_limit",30,30,"https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/","2026-08-26",1),
    # Оренбургская область: 15-30л бензин, чет/нечет
    ("Оренбургская область",None,None,"физлица","even_odd_plates",30,30,"https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/","2026-08-26",1),
    # Мордовия: 40л бензин, чет/нечет
    ("Республика Мордовия",None,None,"физлица","even_odd_plates",40,40,"https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/","2026-08-26",1),
    # Курская область: 30-50л, чет/нечет по началу
    ("Курская область",None,None,"физлица","even_odd_plates_start",50,50,"https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/","2026-08-26",1),
    # Липецкая область: 30л бензин, чет/нечет по началу
    ("Липецкая область",None,None,"физлица","even_odd_plates_start",30,30,"https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/","2026-08-26",1),
    # Нижегородская область: 30-60л бензин, чет/нечет по началу
    ("Нижегородская область",None,None,"физлица","even_odd_plates_start",60,60,"https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/","2026-08-26",1),
    # Калмыкия: 50л бензин
    ("Республика Калмыкия",None,None,"физлица","volume_limit",50,50,"https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/","2026-08-26",1),
    # Крым: 20л бензин, 40л дизель, QR-коды
    ("Республика Крым",None,None,"физлица","volume_limit",20,20,"https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/","2026-08-26",1),
    ("Севастополь",None,None,"физлица","volume_limit",20,20,"https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/","2026-08-26",1),
    # Дагестан: 20л бензин, 50л дизель
    ("Республика Дагестан",None,None,"физлица","volume_limit",20,20,"https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/","2026-08-26",1),
    # Карелия: 40л бензин, 60л дизель
    ("Республика Карелия",None,None,"физлица","volume_limit",40,40,"https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/","2026-08-26",1),
    # Ростовская область: 30л бензин
    ("Ростовская область",None,None,"физлица","volume_limit",30,30,"https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/","2026-08-26",1),
    # Самарская область: 40л бензин
    ("Самарская область",None,None,"физлица","volume_limit",40,40,"https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/","2026-08-26",1),
    # Ульяновская область: 40л бензин
    ("Ульяновская область",None,None,"физлица","volume_limit",40,40,"https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/","2026-08-26",1),
    # Иркутская область: 50л/сутки
    ("Иркутская область",None,None,"физлица","volume_limit",50,50,"https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/","2026-08-26",1),
    # Магаданская область: 100л АИ-92/95
    ("Магаданская область",None,None,"физлица","volume_limit",100,100,"https://www.sravni.ru/text/ceny-na-toplivo-3-avgusta-26/","2026-08-26",1),
]

db = sqlite3.connect(DB)
ins = 0
for r in fresh:
    region, city, network, client, ltype, lval, prev, url, date, cur = r
    row = db.execute("SELECT id FROM restrictions WHERE region=? AND limit_type=?", (region, ltype)).fetchone()
    if row:
        db.execute("""UPDATE restrictions SET city=?, network=?, client_type=?, limit_value=?, previous_value=?,
                      source_url=?, source_date=?, is_current=?, updated_at=datetime('now') WHERE id=?""",
                   (city, network, client, lval, prev, url, date, cur, row[0]))
    else:
        db.execute("""INSERT INTO restrictions(region,city,network,client_type,limit_type,limit_value,previous_value,source_url,source_date,is_current,created_at,updated_at)
                      VALUES(?,?,?,?,?,?,?,?,?,?,datetime('now'),datetime('now'))""",
                   (region, city, network, client, ltype, lval, prev, url, date, cur))
    ins += 1

db.commit()
print(f"Inserted/updated {ins} restrictions")
print(f"Active: {db.execute('SELECT COUNT(*) FROM restrictions WHERE is_current=1').fetchone()[0]}")
print(f"Total: {db.execute('SELECT COUNT(*) FROM restrictions').fetchone()[0]}")
sql = "SELECT COUNT(*) FROM restrictions WHERE previous_value IS NOT NULL"
print(f"With prev_value: {db.execute(sql).fetchone()[0]}")
db.close()
