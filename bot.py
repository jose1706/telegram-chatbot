import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # https://tu-app.onrender.com/webhook

PORT = int(os.getenv("PORT", 10000))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📘 Habilidades Digitales", callback_data="curso1")],
        [InlineKeyboardButton("🚀 Emprendimiento", callback_data="curso2")],
        [InlineKeyboardButton("📣 Marketing Digital", callback_data="curso3")],
        [InlineKeyboardButton("📝 Mi progreso", callback_data="progreso")],
    ]

    await update.message.reply_text(
        "👋 *Bienvenido!* Selecciona un curso:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "curso1":
        await query.edit_message_text(
            "📘 Curso 1\n👉 https://t.me/+CANAL1"
        )

    elif query.data == "curso2":
        await query.edit_message_text(
            "🚀 Curso 2\n👉 https://t.me/+CANAL2"
        )

    elif query.data == "curso3":
        await query.edit_message_text(
            "📣 Curso 3\n👉 https://t.me/+CANAL3"
        )

    elif query.data == "progreso":
        await query.edit_message_text("🏅 Sin progreso registrado aún.")


async def registrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✔ OK, he recibido tu mensaje.")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, registrar))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url=f"{WEBHOOK_URL}/webhook"
    )


if __name__ == "__main__":
    main()
