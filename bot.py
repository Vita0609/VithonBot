from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Загружаем переменные из файла .env
load_dotenv()

# Получаем токен из переменной окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Проверка на наличие токена
if not TELEGRAM_TOKEN:
    raise ValueError("Telegram token is not set in the .env file")

# Функция, которая обрабатывает команду /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привет! Я ваш Telegram бот. Чем могу помочь?")

# Функция, которая обрабатывает команду /help
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Этот бот может отвечать на сообщения и выполнять базовые функции.")

# Функция, которая обрабатывает текстовые сообщения
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    update.message.reply_text(f'Вы сказали: {user_message}')

def main() -> None:
    # Создаем приложение с токеном из .env
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Добавляем обработчики для команд /start и /help
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Добавляем обработчик для текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
