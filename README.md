# diesel-limits

Интерактивная карта ограничений и цен на дизельное топливо по регионам России.
Веб-страница (`index.html`) читает два статичных JSON с сервера и рендерит
хороплет через Leaflet + TopoJSON. Дамп JSON делает `dump_data_json.py` из
SQLite-базы; статичный PNG-хитмап для Telegram генерирует `gen_diesel_map.py`.

## Структура

```
index.html              — фронтенд (Leaflet + TopoJSON, dark theme)
dump_data_json.py       — SQLite → /srv/static/data.json
gen_diesel_map.py       — статичный PNG-хитмап для Telegram
publish_diesel_map.py   — отправка PNG в Telegram-канал
send_text.py            — отправка текста в Telegram-канал
```

## Безопасная настройка (обязательно!)

### 1. Telegram-бот

Токен берётся из переменной окружения `TG_BOT_TOKEN` (раньше был в коде — **небезопасно**).

```bash
export TG_BOT_TOKEN='123456:ABC-DEF...'   # от @BotFather
export TG_CHAT_ID='-1001234567890'         # ID канала (опционально)
```

Добавьте эти строки в `~/.bashrc` или в `~/.env` (и `source ~/.env` перед запуском).

> ⚠️ **Если старый токен когда-либо был в git-истории — отзовите его через
> @BotFather** командой `/revoke`. Иначе любой, кто найдёт токен в истории
> коммитов, сможет писать от имени вашего бота.

### 2. Запуск

```bash
# Обновить data.json (для сайта)
python3 dump_data_json.py

# Сгенерировать PNG-хитмап и отправить в Telegram
python3 gen_diesel_map.py
python3 publish_diesel_map.py

# Отправить текст в канал
python3 send_text.py "Сегодня обновлены лимиты в 5 регионах"
```

### 3. Веб-страница

`index.html` ожидает два файла по путям (настройте nginx/другой веб-сервер):

- `/static/russia_topo.json` — TopoJSON регионов России
- `/static/data.json` — цены и ограничения (генерируется `dump_data_json.py`)

Минимальная конфигурация nginx:

```nginx
location /static/ {
    alias /srv/static/;
    add_header Cache-Control "no-cache";
}
location / {
    root /srv/site;
    index index.html;
}
```

## Технологии

- **Frontend**: Leaflet 1.9.4 + topojson-client 3.0.0 (CDN unpkg, с SRI-хешами)
- **Тайлы**: CartoDB `dark_nolabels` (с атрибуцией — обязательно по лицензии)
- **Backend**: Python 3, SQLite
- **Telegram**: requests + Bot API

## Что было улучшено (changelog)

### Безопасность
- ✅ XSS-защита: все данные экранируются через `esc()` перед вставкой в DOM
- ✅ Валидация URL: только `http:`/`https:` (блок `javascript:`, `data:`)
- ✅ `rel="noopener noreferrer"` на внешних ссылках
- ✅ SRI-хеши + pinned версии Leaflet/topojson (защита от компрометации CDN)
- ✅ Telegram-токен вынесен в env-переменную `TG_BOT_TOKEN`
- ✅ Возвращена атрибуция Leaflet/CartoDB (была скрыта — нарушение лицензий)

### Логика
- ✅ **Баг «Последние ограничения»**: было `slice(-30).reverse()` (показывало
  старые), стало `slice(0, 30)` (новые первыми — как и задумано)
- ✅ **Баг «свободная продажа = ЧС»**: убрано `l.includes('свободная')` из
  условия emergency (это не ЧС, а отсутствие ограничений)
- ✅ Нормализация имён регионов на бэке (`dump_data_json.py`)
- ✅ Валидация цен (защита от мусора в БД)
- ✅ Обработка ошибок `fetch`/`init()` с понятным сообщением

### UX
- ✅ Легенда карты (4 статуса с цветами)
- ✅ Tooltip с названием региона при hover
- ✅ Контрастные цвета severity (emergency/strict различимы)
- ✅ Подписи дат и `client_type` в popup
- ✅ `.top-expensive` исправлен: красный фон вместо зелёного

### Доступность (a11y)
- ✅ `role="application"` + `aria-label` на карте
- ✅ `aria-live="polite"` на динамических блоках
- ✅ `<noscript>` для пользователей без JS
- ✅ `prefers-reduced-motion` — отключение анимаций
- ✅ `:focus-visible` стили на ссылках и кнопках
- ✅ Эмодзи в `<span aria-hidden="true">`

### Код
- ✅ Удалён мёртвый код: дубль `getRegionName`, пустой `nameFix`
- ✅ Единый источник истины для severity: объект `SEV`
- ✅ Кеш DOM-ссылок в объекте `els`
- ✅ Валидация чисел через `num()` вместо `parseFloat` inline
- ✅ `.gitignore` расширен (секреты, БД, генерируемые файлы)
