#!/usr/bin/env python3
"""Insert freshly collected restrictions from 21 July 2026 searches."""
import sqlite3

db = sqlite3.connect('/root/diesel_limits/restrictions.db')

new = [
    # From lenta.ru article (7 July 2026) — detailed region-by-region
    ("Москва", None, "Лукойл", "физлица", "объем", "20-30л бензина, только в бак", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Москва", None, "Газпромнефть", "физлица", "объем", "30л бензина, 60л дизеля (город); до 200л дизеля (трасса)", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Москва", None, "Татнефть", "физлица", "объем", "до 30л АИ-95", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Санкт-Петербург", None, "Лукойл/Teboil", "физлица", "объем", "до 60л дизеля; 20-30л бензина; запрещена продажа в канистры", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Московская область", None, "Лукойл", "физлица", "объем", "20-30л бензина в одни руки, только в бак", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Московская область", None, "Газпромнефть", "физлица", "объем", "до 30л бензина, 60л дизеля (город); до 200л дизеля (трасса)", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Республика Адыгея", None, "все АЗС", "физлица", "объем", "лимиты на усмотрение АЗС; канистры разрешены", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Республика Алтай", "Горно-Алтайск, Майминский, Чемальский районы", "все АЗС", "физлица", "объем", "не более 30л бензина и 50л дизеля (с 1 июля по 1 сентября)", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Республика Алтай", "остальные районы", "все АЗС", "физлица", "объем", "не более 50л бензина и 100л дизеля (с 1 июля по 1 сентября)", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Архангельская область", None, "все АЗС", "физлица", "объем", "от 20 до 50л в одни руки; на трассе М-8 — полный бак", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Республика Башкортостан", None, "все АЗС", "физлица", "объем", "максимум 30л; запрещена продажа в канистры", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Белгородская область", None, "все АЗС", "физлица", "объем", "максимум 30л бензина и 60л дизеля; приграничные — канистры разрешены", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Брянская область", None, "все АЗС", "физлица", "объем", "до 20л бензина; запрет на канистры (до 30 июня)", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Владимирская область", None, "все АЗС", "физлица", "объем", "20-30л бензина, 40л дизеля; режим экономии для служебных машин", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Республика Дагестан", None, "все АЗС", "физлица", "объем", "не более 20л бензина и 50л дизеля в одни руки", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Забайкальский край", None, "все АЗС", "физлица", "объем", "не более 15л в бак; режим повышенной готовности", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Республика Карелия", None, "АЗС", "физлица", "объем", "от 20 до 60л в руки; с 4 июля — мин. лимит 10л", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Краснодарский край", None, "все АЗС", "физлица", "объем", "20-30л бензина, 30-60л дизеля; с 03:00 до 06:00 — только экстренные службы", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Красноярский край", None, "Газпромнефть", "физлица", "объем", "20-40л бензина, 40-80л дизеля (трасса до 200л); запрещены канистры", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),
    ("Республика Крым", None, "все АЗС", "все", "запрет", "продажа только госслужбам; физлицам и юрлицам — полностью прекращена", "https://lenta.ru/articles/2026/07/07/prodazha-benzina-ogranicheniya/", "2026-07-07"),

    # From t-j.ru (17 July 2026) — latest updates
    ("Тамбовская область", None, "все АЗС", "физлица", "время", "с 20 июля — заправка по четным/нечетным дням (по первой цифре госномера)", "https://t-j.ru/news/kakie-regiony-bez-benza/", "2026-07-17"),
    ("Орловская область", None, "все АЗС", "физлица", "объем", "не более 30л; дизель без ограничений; график по номерам отменен 16 июля", "https://t-j.ru/news/kakie-regiony-bez-benza/", "2026-07-17"),
    ("Курская область", None, "все АЗС", "физлица", "время", "с 15 июля — заправка по четным/нечетным дням (по первой цифре номера)", "https://t-j.ru/news/kakie-regiony-bez-benza/", "2026-07-17"),
    ("Ростовская область", None, "все АЗС", "физлица", "объем", "не более 30л бензина, 60л дизеля (легк); 200л дизеля (груз); 300л (пасс.транспорт)", "https://t-j.ru/news/kakie-regiony-bez-benza/", "2026-07-17"),
    ("Кировская область", None, "все АЗС", "физлица", "время", "с 11 июля — заправка по четным/нечетным дням", "https://t-j.ru/news/kakie-regiony-bez-benza/", "2026-07-17"),
    ("Астраханская область", None, "все АЗС", "физлица", "время", "с 9 июля — график по последней цифре номера", "https://t-j.ru/news/kakie-regiony-bez-benza/", "2026-07-17"),
    ("Новосибирская область", None, "все АЗС", "физлица", "объем", "не более 30л бензина, 60л дизеля на машину", "https://t-j.ru/news/kakie-regiony-bez-benza/", "2026-07-17"),
    ("Нижегородская область", None, "все АЗС", "физлица", "объем", "40л бензина в одни руки; планируется введение QR-кодов", "https://t-j.ru/news/kakie-regiony-bez-benza/", "2026-07-17"),
    ("Республика Саха (Якутия)", None, "Саханефтегазсбыт", "физлица", "объем", "30л бензина, 200л дизеля; запрещена продажа в тару", "https://t-j.ru/news/kakie-regiony-bez-benza/", "2026-07-17"),
    ("Приморский край", None, "все АЗС", "юрлица/грузовики", "объем", "до 100л в городе, до 200л на трассе для большегрузов", "https://t-j.ru/news/kakie-regiony-bez-benza/", "2026-07-17"),
    ("Ульяновская область", None, "все АЗС", "физлица", "объем", "не более 40л бензина, 100л дизеля (легк); 300л дизеля (груз)", "https://t-j.ru/news/kakie-regiony-bez-benza/", "2026-07-17"),
    ("Курганская область", None, "все АЗС", "физлица", "объем", "не более 40л бензина, 80л дизеля (город); до 200л дизеля (трасса)", "https://t-j.ru/news/kakie-regiony-bez-benza/", "2026-07-17"),
    ("Вологодская область", None, "Лукойл", "физлица", "объем", "30л бензина, 60л дизеля (город); 200л дизеля (трасса); только в бак", "https://t-j.ru/news/kakie-regiony-bez-benza/", "2026-07-17"),
    ("Пензенская область", None, "все АЗС", "физлица", "объем", "до 100л бензина, 200л дизеля на машину", "https://t-j.ru/news/kakie-regiony-bez-benza/", "2026-07-17"),
    ("Саратовская область", None, "все АЗС", "физлица", "объем", "максимум 30л бензина на машину (с 23 по 30 июня)", "https://t-j.ru/news/kakie-regiony-bez-benza/", "2026-07-17"),
    ("Омская область", None, "все АЗС", "физлица", "объем", "40л бензина, 80л дизеля; на трассе до 200л дизеля", "https://t-j.ru/news/kakie-regiony-bez-benza/", "2026-07-17"),
    ("Кемеровская область", None, "Газпромнефть", "физлица", "объем", "до 40л бензина, 80л дизеля; на трассе до 200л дизеля", "https://t-j.ru/news/kakie-regiony-bez-benza/", "2026-07-17"),

    # From rbc.ru
    ("Россия (федеральный уровень)", None, "правительство РФ", "все", "запрет", "запрет экспорта дизтоплива до 31 августа 2026", "https://www.rbc.ru/economics/03/07/2026/6a461d589a79474020d03021", "2026-07-03"),
]

inserted = 0
updated = 0
for r in new:
    region, city, network, client_type, limit_type, limit_value, src_url, src_date = r
    try:
        db.execute(
            """INSERT INTO restrictions(region,city,network,client_type,limit_type,limit_value,source_url,source_date,is_current,created_at,updated_at)
               VALUES(?,?,?,?,?,?,?,?,1,datetime('now'),datetime('now'))""",
            (region, city, network, client_type, limit_type, limit_value, src_url, src_date)
        )
        inserted += 1
    except Exception as e:
        updated += 1

db.commit()
print(f"Inserted: {inserted}, updated: {updated}")
db.close()
