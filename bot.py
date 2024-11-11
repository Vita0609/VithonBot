import logging
from dotenv import load_dotenv
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import requests
import sqlite3

# Настроим логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Загружаем переменные из файла .env
load_dotenv()

# Получаем токен из переменной окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
api_key = os.getenv("API_KEY")

# Проверка на наличие токена
if not TELEGRAM_TOKEN:
    raise ValueError("Telegram token is not set in the .env file")

# Функция для получения погоды
def get_weather(city):
    # Проверяем, что API-ключ был успешно получен
    if not api_key:
        return "API-ключ не найден!"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if data.get("main"):
        temperature = data["main"]["temp"]
        return f"Температура в {city}: {temperature - 273.15:.2f}°C"
    else:
        return "Не удалось получить данные о погоде."

# Создание базы данных для пользователей
def create_db():
    with sqlite3.connect('bot_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)''')
        conn.commit()

# Добавление пользователя в базу данных
def add_user(user_id, username):
    with sqlite3.connect('bot_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (id, username) VALUES (?, ?)', (user_id, username))
        conn.commit()

# Функция обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Помощь", callback_data='help')],
        [InlineKeyboardButton("О боте", callback_data='about')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Привет! Я ваш Telegram бот. Чем могу помочь?", reply_markup=reply_markup)

# Функция обработки команды /help
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Этот бот может отвечать на сообщения и выполнять базовые функции.")

# Функция обработки команды /about
def about(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Этот бот был создан для демонстрации работы с Telegram API.")

# Функция для регистрации пользователей
def register(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    add_user(user_id, username)
    update.message.reply_text(f"Вы успешно зарегистрированы: {username}")

# Функция для получения погоды
def weather(update: Update, context: CallbackContext) -> None:
    city = " ".join(context.args)  # Получаем город из аргументов команды
    weather_info = get_weather(city)
    update.message.reply_text(weather_info)

# Функция обработки текстовых сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    update.message.reply_text(f'Вы сказали: {user_message}')

def main() -> None:
    # Создаем приложение с токеном из .env
    create_db()  # Создаем базу данных при старте
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Добавляем обработчики для команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("register", register))
    application.add_handler(CommandHandler("weather", weather))

    # Добавляем обработчик для текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
