#!/usr/bin/env python3
"""Diesel availability+price heatmap. Ponytail: minimal."""
import csv, re
from collections import defaultdict
from datetime import datetime
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt; import numpy as np

ROOT = "/root/diesel_limits"

# ── 1. Try CSV overlay (optional) ──
csv_avg = {}
csv_path = "/root/.hermes/cache/documents/doc_24fb17103de8_purchases - 2026-07-03T154633.262.csv"
try:
    with open(csv_path, encoding="cp1251") as f:
        csv_prices = defaultdict(list)
        for row in csv.reader(f, delimiter=";"):
            if len(row) < 23: continue
            p = row[14].strip().replace(",",".")
            r = row[22].strip()
            if p and r:
                try: csv_prices[r].append(float(p))
                except: pass
        csv_avg = {r: round(sum(v)/len(v),2) for r,v in csv_prices.items() if v}
except FileNotFoundError:
    pass

# ── 2. Росстат цены (6 июля 2026) — основной источник ──
base = {
    "Москва":80.41,"Санкт-Петербург":80.06,"Алтайский край":84.29,"Амурская область":91.32,
    "Архангельская область":83.48,"Астраханская область":78.92,"Белгородская область":76.86,
    "Брянская область":81.52,"Владимирская область":88.37,"Волгоградская область":77.38,
    "Вологодская область":91.31,"Воронежская область":90.83,"Еврейская АО":90.73,"Забайкальский край":96.52,
    "Ивановская область":83.62,"Иркутская область":92.49,"Калининградская область":83.68,
    "Калужская область":79.59,"Камчатский край":106.78,"Кемеровская область":85.32,
    "Кировская область":83.58,"Костромская область":90.96,"Краснодарский край":82.89,
    "Красноярский край":89.63,"Курганская область":82.41,"Курская область":83.56,
    "Ленинградская область":83.18,"Липецкая область":83.09,"Магаданская область":107.09,
    "Московская область":82.45,"Мурманская область":88.45,"Ненецкий АО":86.77,
    "Нижегородская область":81.10,"Новгородская область":80.17,"Новосибирская область":88.71,
    "Омская область":79.13,"Оренбургская область":79.32,"Орловская область":77.00,
    "Пензенская область":80.38,"Пермский край":87.91,"Приморский край":91.71,"Псковская область":80.26,
    "Республика Адыгея":80.99,"Республика Алтай":90.04,"Республика Башкортостан":77.52,
    "Республика Бурятия":85.64,"Республика Дагестан":96.80,"Республика Ингушетия":76.58,
    "Республика Калмыкия":104.01,"Республика Карелия":86.68,"Республика Коми":84.29,
    "Республика Марий Эл":85.40,"Республика Мордовия":80.42,"Республика Саха (Якутия)":97.25,
    "Республика Северная Осетия — Алания":77.79,"Республика Татарстан":81.57,
    "Республика Тыва":117.19,"Республика Хакасия":89.31,"Ростовская область":81.04,
    "Рязанская область":84.71,"Самарская область":86.94,"Сахалинская область":100.20,
    "Свердловская область":85.60,"Смоленская область":80.53,"Ставропольский край":79.88,
    "Тамбовская область":91.16,"Тверская область":82.11,"Томская область":89.60,
    "Тульская область":89.68,"Тюменская область":91.95,"Удмуртская Республика":78.77,
    "Ульяновская область":78.30,"Хабаровский край":88.59,"Ханты-Мансийский АО — Югра":93.28,
    "Челябинская область":79.92,"Чеченская Республика":98.78,"Чувашская Республика":81.77,
    "Чукотский АО":78.00,"Ямало-Ненецкий АО":83.01,"Ярославская область":77.85,
    "Кабардино-Балкарская Республика":94.87,"Карачаево-Черкесская Республика":75.13,
    "Республика Крым":139.15,"Севастополь":150.49,
}

# Map CSV names to canonical
alias = {"Чувашская республика":"Чувашская Республика","Удмуртская республика":"Удмуртская Республика",
         "Ханты-Мансийский автономный округ":"Ханты-Мансийский АО — Югра",
         "Ямало-Ненецкий автономный округ":"Ямало-Ненецкий АО","Еврейская автономная область":"Еврейская АО"}
for csv_name, price in csv_avg.items():
    canon = alias.get(csv_name, csv_name)
    if canon in base:
        base[canon] = price  # overwrite with CSV data

# ── 3. Restrictions: читаем level из data.json (синхронизировано с интерактивной картой) ──
import json
levels = {}
try:
    with open("/srv/static/data.json") as f:
        for r in json.load(f).get("regions", []):
            if "region" in r and "level" in r:
                levels[r["region"]] = r["level"]
except Exception:
    pass
# interactive level → PNG status code (1=unknown,2=soft,3=tight,4=critical)
def _sc(lvl):
    if lvl is None or lvl <= 0: return 1
    if lvl <= 2: return 2
    if lvl == 3: return 3
    return 4  # level 4 = дефицит/ЧС
status_cmap = {1:(0.91,0.66,0.22),2:(0.83,0.36,0.17),3:(0.70,0.13,0.13),4:(0.50,0,0)}

# ── 4. Build heatmap ──
sorted_regions = sorted(base.items(), key=lambda x: x[0])  # ponytail: alphabetical, not geographic
cols = 13
rows = int(np.ceil(len(sorted_regions)/cols))
fig, ax = plt.subplots(figsize=(20,14))
fig.patch.set_facecolor('#1a1a2e'); ax.set_facecolor('#1a1a2e')
norm = matplotlib.colors.Normalize(vmin=74, vmax=104)
cmap = plt.cm.RdYlGn_r

for i,(name,price) in enumerate(sorted_regions):
    r,c = divmod(i,cols)
    sc = _sc(levels.get(name))
    base_col = np.array(status_cmap[sc])
    price_col = np.array(cmap(norm(price))[:3])
    if sc >= 4:
        color = base_col  # pure status color for emergency
    else:
        color = np.clip(0.7*base_col + 0.3*price_col, 0, 1)
    rect = plt.Rectangle((c,rows-1-r),0.95,0.95,facecolor=color,edgecolor='#444',linewidth=0.5)
    ax.add_patch(rect)
    lum = 0.299*color[0] + 0.587*color[1] + 0.114*color[2]
    tc = 'black' if lum>0.55 else 'white'
    # Short name
    s = name.replace("Республика ","Р.").replace("область","обл.").replace("автономный округ","АО")
    s = s.replace("Ханты-Мансийский АО — Югра","ХМАО").replace("Ямало-Ненецкий АО","ЯНАО")
    s = s.replace("Чукотский АО","Чукотка").replace("Еврейская АО","ЕАО")
    s = s.replace("Забайкальский край","Забайкалье").replace("Приморский край","Приморье")
    s = s.replace("Камчатский край","Камчатка").replace("Красноярский край","Красноярск")
    s = s.replace("Хабаровский край","Хабаровск").replace("Ставропольский край","Ставрополь")
    s = s.replace("Республика Саха (Якутия)","Якутия").replace("Удмуртская Республика","Удмуртия")
    s = s.replace("Чувашская Республика","Чувашия").replace("Кабардино-Балкарская Республика","КБР")
    s = s.replace("Карачаево-Черкесская Республика","КЧР")
    s = s.replace("Северная Осетия — Алания","Сев.Осетия").replace("Чеченская Республика","Чечня")
    ax.text(c+0.475,rows-1-r+0.5,f"{s}\n{price:.0f}₽",ha='center',va='center',fontsize=5.5,fontweight='bold',color=tc)

ax.set_xlim(0,cols); ax.set_ylim(0,rows); ax.axis('off')
ax.set_title(f"ДИЗЕЛЬ: ДОСТУПНОСТЬ И ЦЕНЫ ПО РЕГИОНАМ — {datetime.now():%d.%m.%Y}",fontsize=18,fontweight='bold',color='white',pad=20)

legend = [plt.Rectangle((0,0),1,1,facecolor=status_cmap[i]) for i in range(1,5)]
labels = ["незн.ограничения","лимиты","жёсткие <60л","дефицит/ЧС"]
ax.legend(legend,labels,loc='lower center',bbox_to_anchor=(0.5,-0.06),ncol=5,frameon=False,fontsize=8,labelcolor='white')

csv_n = len(csv_avg)
today = datetime.now().strftime("%d.%m.%Y")
n_restr = sum(1 for v in levels.values() if v is not None and v >= 2)
stats = (f"Цвет: статус (70%) + цена (30%) | Цены: Росстат + {csv_n} рег. из транзакций ({today}) | "
         f"Средняя ДТ: {np.mean([p for _,p in sorted_regions]):.1f} ₽/л | "
         f"Ограничения: {n_restr}+ регионов | {today}")
ax.text(0.5,-0.15,stats,transform=ax.transAxes,ha='center',va='top',fontsize=8,color='#aaa',style='italic')

plt.tight_layout()
out = f"{ROOT}/tmp/diesel_heatmap.png"
fig.savefig(out,dpi=400,bbox_inches='tight',facecolor=fig.get_facecolor())
print(f"Saved: {out}  Regions: {len(base)}  CSV overlays: {csv_n}  Restricted: {n_restr}")
