from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

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

    application = Application.builder().token("7843473453:AAExbQMtCWf5UWXt66PdcNNRnuEJpvkn4JU").build()

    # Добавляем обработчики для команд /start и /help
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    # Добавляем обработчик для текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
