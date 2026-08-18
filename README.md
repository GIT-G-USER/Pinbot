# zakrep-bot

Бот закрепляет сообщения по команде `/zakrep`, не снимая уже закреплённые
(Telegram позволяет держать несколько закреплённых сообщений одновременно).

## Команды
- `/nachatzakrep` — приветствие и справка
- `/zakrep` — ответь на нужное сообщение, оно добавится в закреп (`/zakrep tiho` — без уведомления)
- `/otkrep` — открепить только то сообщение, на которое ответил
- `/spisok` — показать последнее закреплённое

Бот должен быть админом чата с правом «Закреплять сообщения».

## Локальный запуск
```bash
pip install -r requirements.txt
python bot.py   # токен впиши в переменную TOKEN в bot.py
```

## Деплой на Railway (работает 24/7)
1. Залей эту папку в репозиторий на GitHub (файл `.gitignore` уже есть; токен в коде не храни — на Railway используем переменную окружения).
2. Зайди на https://railway.app → New Project → Deploy from GitHub repo → выбери репозиторий.
3. Вкладка Variables → New Variable: `TELEGRAM_BOT_TOKEN` = токен от @BotFather.
4. Railway сам поставит зависимости из `requirements.txt` и запустит процесс из `Procfile` (`worker: python bot.py`).
5. Logs покажут `Application started` — бот онлайн постоянно, компьютер выключать можно.

Важно: одновременно должна работать только одна копия бота (иначе Telegram выдаст
ошибку `Conflict: terminated by other getUpdates request`) — останови локальный
запуск, когда бот работает на Railway.
