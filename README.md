# phc-pysqltelegram
Python + SQLite3 for telegram bot. Made that just to educate, if you need it to copy -- ur welcome!)))

# Telegram Registration Bot 🤖

Python Telegram бот для регистрации пользователей с SQLite базой данных.

## 🚀 Возможности

- Регистрация пользователей
- Хранение данных в SQLite
- Просмотр списка пользователей
- Безопасные параметризованные запросы
- Логирование операций

## 📦 Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/PHCNMDco/phc-pysqltelegram.git
cd phc-pysqltelegram

Установите зависимости:

bash
pip install -r requirements.txt
Создайте бота через @BotFather и получите токен

Создайте файл конфигурации:

bash
cp config.example.py config.py
Отредактируйте config.py с вашим токеном

Запустите бота:

bash
python src/bot.py
🛠️ Использование
Отправьте боту команду /start

Введите ваше имя

Введите пароль

Нажмите "Список пользователей" для просмотра всех зарегистрированных

🏗️ Архитектура
bot.py - Основной класс бота

SQLite - База данных для хранения

pyTelegramBotAPI - Работа с Telegram API

🔒 Безопасность
Параметризованные SQL запросы

Валидация ввода

Логирование ошибок

📝 Лицензия
MIT License - смотрите файл LICENSE

text

## 7. Для запуска (после настройки config.py)

```python
# config.py
BOT_TOKEN = "1234567890:AAFabcdefghijklmnopqrstuvwxyz"  # Твой реальный токен
DATABASE_NAME = "yourDB.sql"
