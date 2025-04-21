from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

ADMIN_ID = 6154300723  # Замените на ваш Telegram ID (узнать у @userinfobot)
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Токен берётся из переменных окружения
KEYS_FILE = "keys.txt"

# Создаем файл, если он не существует
if not os.path.exists(KEYS_FILE):
    open(KEYS_FILE, 'a').close()

def start(update, context):
    update.message.reply_text(
        "🔑 Бот для управления ключами.\n\n"
        "Доступные команды:\n"
        "/addkey <ключ> <serialhash> - добавить ключ\n"
        "/delkey <ключ> - удалить ключ\n"
        "/listkeys - список всех ключей\n"
        "/clearkeys - очистить все ключи"
    )

def add_key(update, context):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        update.message.reply_text("❌ Доступ запрещён!")
        return

    try:
        _, key, serialhash = update.message.text.split(maxsplit=2)
    except ValueError:
        update.message.reply_text("⚠ Используйте: /addkey <ключ> <serialhash>")
        return

    with open(KEYS_FILE, "a") as f:
        f.write(f"{key}:{serialhash}\n")

    update.message.reply_text(f"✅ Добавлено: `{key}:{serialhash}`", parse_mode="Markdown")

def delete_key(update, context):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        update.message.reply_text("❌ Доступ запрещён!")
        return

    try:
        _, key_to_delete = update.message.text.split(maxsplit=1)
    except ValueError:
        update.message.reply_text("⚠ Используйте: /delkey <ключ>")
        return

    # Читаем все ключи
    with open(KEYS_FILE, "r") as f:
        lines = f.readlines()

    # Фильтруем ключи, оставляя все кроме удаляемого
    new_lines = [line for line in lines if not line.startswith(key_to_delete + ":")]

    # Если количество строк уменьшилось - ключ был удален
    if len(new_lines) < len(lines):
        with open(KEYS_FILE, "w") as f:
            f.writelines(new_lines)
        update.message.reply_text(f"✅ Ключ `{key_to_delete}` удален", parse_mode="Markdown")
    else:
        update.message.reply_text(f"❌ Ключ `{key_to_delete}` не найден", parse_mode="Markdown")

def list_keys(update, context):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        update.message.reply_text("❌ Доступ запрещён!")
        return

    try:
        with open(KEYS_FILE, "r") as f:
            keys = f.readlines()
    except FileNotFoundError:
        update.message.reply_text("❌ Файл с ключами не найден")
        return

    if not keys:
        update.message.reply_text("📭 Список ключей пуст")
    else:
        keys_list = "".join([f"🔑 {key}" for key in keys])
        update.message.reply_text(f"📋 Список ключей:\n\n{keys_list}")

def clear_keys(update, context):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        update.message.reply_text("❌ Доступ запрещён!")
        return

    open(KEYS_FILE, "w").close()
    update.message.reply_text("✅ Все ключи удалены")

updater = Updater(BOT_TOKEN)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("addkey", add_key))
dispatcher.add_handler(CommandHandler("delkey", delete_key))
dispatcher.add_handler(CommandHandler("listkeys", list_keys))
dispatcher.add_handler(CommandHandler("clearkeys", clear_keys))
updater.start_polling()
updater.idle()