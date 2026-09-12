#!/usr/bin/env python3
import sqlite3
from datetime import datetime as dt

today = dt.now().strftime("%Y-%m-%d")
db = sqlite3.connect('/root/diesel_limits/restrictions.db')

# ==== 1. Prices (Rosstat, July 13 2026) ====
prices_data = {
    "Altajskij kraj":87.87, "Amurskaja oblast":92.19, "Arhangelskaja oblast":83.68,
    "Astrahanskaja oblast":79.39, "Belgorodskaja oblast":77.12, "Brjanskaja oblast":81.81,
    "Vladimirskaja oblast":89.99, "Volgogradskaja oblast":78.15, "Vologodskaja oblast":91.94,
    "Voronezhskaja oblast":97.28, "Evrejskaja AO":90.73, "Zabajkalskij kraj":97.42,
    "Ivanovskaja oblast":83.81, "Irkutskaja oblast":92.97, "Kabardino-Balkarskaja Respublika":98.26,
    "Kaliningradskaja oblast":84.06, "Kaluzhskaja oblast":84.58, "Kamchatskij kraj":106.78,
    "Karachaevo-Cherkesskaja Respublika":75.39, "Kemerovskaja oblast":86.64, "Kirovskaja oblast":84.36,
    "Kostromskaja oblast":96.77, "Krasnodarskij kraj":83.66, "Krasnojarskij kraj":91.42,
    "Kurganskaja oblast":82.55, "Kurskaja oblast":84.37, "Leningradskaja oblast":83.38,
    "Lipeckaja oblast":86.18, "Magadanskaja oblast":116.37, "Moskva":81.05,
    "Moskovskaja oblast":83.53, "Murmanskaja oblast":88.72, "Neneckij AO":87.78,
    "Nizhegorodskaja oblast":82.50, "Novgorodskaja oblast":80.56, "Novosibirskaja oblast":93.17,
    "Omskaja oblast":79.30, "Orenburgskaja oblast":79.47, "Orlovskaja oblast":77.22,
    "Penzenskaja oblast":81.14, "Permskij kraj":89.44, "Primorskij kraj":92.18,
    "Pskovskaja oblast":80.65, "Respublika Adygeja":81.30, "Respublika Altaj":93.19,
    "Respublika Bashkortostan":77.75, "Respublika Burjatija":85.71, "Respublika Dagestan":100.49,
    "Respublika Ingushetija":78.11, "Respublika Kalmykija":108.94, "Respublika Karelija":86.96,
    "Respublika Komi":93.48, "Respublika Krym":186.20, "Respublika Marij El":90.77,
    "Respublika Mordovija":80.63, "Respublika Saha (Jakutija)":99.86,
    "Respublika Severnaja Osetija - Alanija":78.32, "Respublika Tatarstan":81.65,
    "Respublika Tyva":122.86, "Respublika Hakasija":97.43, "Rostovskaja oblast":81.92,
    "Rjazanskaja oblast":86.68, "Samarskaja oblast":87.46, "Sankt-Peterburg":80.58,
    "Saratovskaja oblast":87.51, "Sahalinskaja oblast":100.31, "Sverdlovskaja oblast":86.08,
    "Sevastopol":218.44, "Smolenskaja oblast":80.84, "Stavropolskij kraj":91.26,
    "Tambovskaja oblast":92.72, "Tverskaja oblast":82.18, "Tomskaja oblast":90.82,
    "Tulskaja oblast":92.57, "Tjumenskaja oblast":95.99, "Udmurtskaja Respublika":78.97,
    "Uljanovskaja oblast":78.65, "Habarovskij kraj":88.59, "Hanty-Mansijskij AO - Jugra":97.21,
    "Cheljabinskaja oblast":80.65, "Chechenskaja Respublika":99.72, "Chuvashskaja Respublika":85.09,
    "Chukotskij AO":78.00, "Jamalo-Neneckij AO":83.37, "Jaroslavskaja oblast":78.07,
}

# Map transliterated keys to full russian names
ru_names = {
    "Altajskij kraj": "Altajskij kraj",
    "Amurskaja oblast": "Amurskaja oblast",
    "Arhangelskaja oblast": "Arhangelskaja oblast",
    "Astrahanskaja oblast": "Astrahanskaja oblast",
    "Belgorodskaja oblast": "Belgorodskaja oblast",
    "Brjanskaja oblast": "Brjanskaja oblast",
    "Vladimirskaja oblast": "Vladimirskaja oblast",
    "Volgogradskaja oblast": "Volgogradskaja oblast",
    "Vologodskaja oblast": "Vologodskaja oblast",
    "Voronezhskaja oblast": "Voronezhskaja oblast",
    "Evrejskaja AO": "Evrejskaja AO",
    "Zabajkalskij kraj": "Zabajkalskij kraj",
    "Ivanovskaja oblast": "Ivanovskaja oblast",
    "Irkutskaja oblast": "Irkutskaja oblast",
    "Kabardino-Balkarskaja Respublika": "Kabardino-Balkarskaja Respublika",
    "Kaliningradskaja oblast": "Kaliningradskaja oblast",
    "Kaluzhskaja oblast": "Kaluzhskaja oblast",
    "Kamchatskij kraj": "Kamchatskij kraj",
    "Karachaevo-Cherkesskaja Respublika": "Karachaevo-Cherkesskaja Respublika",
    "Kemerovskaja oblast": "Kemerovskaja oblast",
    "Kirovskaja oblast": "Kirovskaja oblast",
    "Kostromskaja oblast": "Kostromskaja oblast",
    "Krasnodarskij kraj": "Krasnodarskij kraj",
    "Krasnojarskij kraj": "Krasnojarskij kraj",
    "Kurganskaja oblast": "Kurganskaja oblast",
    "Kurskaja oblast": "Kurskaja oblast",
    "Leningradskaja oblast": "Leningradskaja oblast",
    "Lipeckaja oblast": "Lipeckaja oblast",
    "Magadanskaja oblast": "Magadanskaja oblast",
    "Moskva": "Moskva",
    "Moskovskaja oblast": "Moskovskaja oblast",
    "Murmanskaja oblast": "Murmanskaja oblast",
    "Neneckij AO": "Neneckij AO",
    "Nizhegorodskaja oblast": "Nizhegorodskaja oblast",
    "Novgorodskaja oblast": "Novgorodskaja oblast",
    "Novosibirskaja oblast": "Novosibirskaja oblast",
    "Omskaja oblast": "Omskaja oblast",
    "Orenburgskaja oblast": "Orenburgskaja oblast",
    "Orlovskaja oblast": "Orlovskaja oblast",
    "Penzenskaja oblast": "Penzenskaja oblast",
    "Permskij kraj": "Permskij kraj",
    "Primorskij kraj": "Primorskij kraj",
    "Pskovskaja oblast": "Pskovskaja oblast",
    "Respublika Adygeja": "Respublika Adygeja",
    "Respublika Altaj": "Respublika Altaj",
    "Respublika Bashkortostan": "Respublika Bashkortostan",
    "Respublika Burjatija": "Respublika Burjatija",
    "Respublika Dagestan": "Respublika Dagestan",
    "Respublika Ingushetija": "Respublika Ingushetija",
    "Respublika Kalmykija": "Respublika Kalmykija",
    "Respublika Karelija": "Respublika Karelija",
    "Respublika Komi": "Respublika Komi",
    "Respublika Krym": "Respublika Krym",
    "Respublika Marij El": "Respublika Marij El",
    "Respublika Mordovija": "Respublika Mordovija",
    "Respublika Saha (Jakutija)": "Respublika Saha (Jakutija)",
    "Respublika Severnaja Osetija - Alanija": "Respublika Severnaja Osetija - Alanija",
    "Respublika Tatarstan": "Respublika Tatarstan",
    "Respublika Tyva": "Respublika Tyva",
    "Respublika Hakasija": "Respublika Hakasija",
    "Rostovskaja oblast": "Rostovskaja oblast",
    "Rjazanskaja oblast": "Rjazanskaja oblast",
    "Samarskaja oblast": "Samarskaja oblast",
    "Sankt-Peterburg": "Sankt-Peterburg",
    "Saratovskaja oblast": "Saratovskaja oblast",
    "Sahalinskaja oblast": "Sahalinskaja oblast",
    "Sverdlovskaja oblast": "Sverdlovskaja oblast",
    "Sevastopol": "Sevastopol",
    "Smolenskaja oblast": "Smolenskaja oblast",
    "Stavropolskij kraj": "Stavropolskij kraj",
    "Tambovskaja oblast": "Tambovskaja oblast",
    "Tverskaja oblast": "Tverskaja oblast",
    "Tomskaja oblast": "Tomskaja oblast",
    "Tulskaja oblast": "Tulskaja oblast",
    "Tjumenskaja oblast": "Tjumenskaja oblast",
    "Udmurtskaja Respublika": "Udmurtskaja Respublika",
    "Uljanovskaja oblast": "Uljanovskaja oblast",
    "Habarovskij kraj": "Habarovskij kraj",
    "Hanty-Mansijskij AO - Jugra": "Hanty-Mansijskij AO - Jugra",
    "Cheljabinskaja oblast": "Cheljabinskaja oblast",
    "Chechenskaja Respublika": "Chechenskaja Respublika",
    "Chuvashskaja Respublika": "Chuvashskaja Respublika",
    "Chukotskij AO": "Chukotskij AO",
    "Jamalo-Neneckij AO": "Jamalo-Neneckij AO",
    "Jaroslavskaja oblast": "Jaroslavskaja oblast",
}

url = "https://rosstat.gov.ru/storage/mediabank/107_15-07-2026.html"
count_upd = 0
for key, price in prices_data.items():
    region = ru_names[key]
    db.execute(
        "INSERT OR REPLACE INTO prices(region,price,source_url,source_date,updated_at) VALUES(?,?,?,?,datetime('now'))",
        (region, price, url, '13.07.2026')
    )
    count_upd += 1
print(f"Prices updated: {count_upd} regions")

for key, price in prices_data.items():
    region = ru_names[key]
    db.execute(
        "INSERT OR IGNORE INTO prices_history(region,date,price) VALUES(?,?,?)",
        (region, today, float(price))
    )
print(f"History entries added: {len(prices_data)}")

db.commit()
db.close()
print("DB update complete")
