import telebot
import sqlite3
import logging
from typing import List, Tuple

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.bot = telebot.TeleBot('YOUR_BOT_TOKEN')
        self.db_name = 'yourDB.sql'
        self.setup_handlers()
    
    def setup_handlers(self):
        """Настройка обработчиков сообщений"""
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.init_database()
            self.bot.send_message(message.chat.id, 
                                'Привет, сейчас мы тебя зарегистрируем! Введите ваше имя')
            self.bot.register_next_step_handler(message, self.user_name)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback(call):
            if call.data == 'users':
                self.show_users(call)

    def init_database(self):
        """Инициализация базы данных"""
        try:
            conn = sqlite3.connect(self.db_name)
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(50) NOT NULL,
                    pass VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
        finally:
            if conn:
                conn.close()

    def user_name(self, message):
        """Обработка имени пользователя"""
        name = message.text.strip()
        
        self.bot.send_message(message.chat.id, 'Введите пароль')
        self.bot.register_next_step_handler(
            message, 
            lambda msg: self.user_pass(msg, name)
        )

    def user_pass(self, message, name: str):
        """Обработка пароля и сохранение пользователя"""
        password = message.text.strip()
        
        if self.save_user(name, password):
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(
                'Список пользователей', 
                callback_data='users'
            ))
            self.bot.send_message(
                message.chat.id, 
                'Пользователь успешно зарегистрирован!',
                reply_markup=markup
            )
        else:
            self.bot.send_message(
                message.chat.id, 
                'Ошибка при регистрации. Попробуйте снова.'
            )

    def save_user(self, name: str, password: str) -> bool:
        """Сохранение пользователя в базу данных"""
        try:
            conn = sqlite3.connect(self.db_name)
            cur = conn.cursor()
            
            # Используем параметризованные запросы для безопасности
            cur.execute(
                "INSERT INTO users (name, pass) VALUES (?, ?)",
                (name, password)
            )
            conn.commit()
            return True
            
        except sqlite3.Error as e:
            logger.error(f"Error saving user: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def show_users(self, call):
        """Показать список пользователей"""
        try:
            users = self.get_all_users()
            
            if users:
                info = "Список пользователей:\n\n"
                for user in users:
                    info += f"ID: {user[0]}, Имя: {user[1]}, Пароль: {user[2]}\n"
            else:
                info = "Пользователи не найдены"
                
            self.bot.send_message(call.message.chat.id, info)
            
        except Exception as e:
            logger.error(f"Error showing users: {e}")
            self.bot.send_message(call.message.chat.id, "Ошибка при получении данных")

    def get_all_users(self) -> List[Tuple]:
        """Получить всех пользователей из базы"""
        try:
            conn = sqlite3.connect(self.db_name)
            cur = conn.cursor()
            cur.execute('SELECT * FROM users')
            return cur.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error getting users: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def run(self):
        """Запуск бота"""
        logger.info("Bot started...")
        self.bot.polling(none_stop=True)

if __name__ == "__main__":
    bot = TelegramBot()
    bot.run()
