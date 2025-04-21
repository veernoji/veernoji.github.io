from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

ADMIN_ID = 6154300723  # Замените на ваш Telegram ID (узнать у @userinfobot)
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Токен берётся из переменных окружения

def start(update, context):
    update.message.reply_text(
        "🔑 Бот для управления ключами.\n"
        "Добавить ключ: /addkey <ключ> <serialhash>"
    )

def add_key(update, context):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        update.message.reply_text("❌ Доступ запрещён!")
        return

    # Проверяем, что введены оба параметра
    try:
        _, key, serialhash = update.message.text.split(maxsplit=2)
    except ValueError:
        update.message.reply_text("⚠ Используйте: /addkey <ключ> <serialhash>")
        return

    # Записываем в формате key:serialhash
    with open("keys.txt", "a") as f:
        f.write(f"{key}:{serialhash}\n")

    update.message.reply_text(f"✅ Добавлено: `{key}:{serialhash}`", parse_mode="Markdown")

updater = Updater(BOT_TOKEN)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("addkey", add_key))
updater.start_polling()
updater.idle()