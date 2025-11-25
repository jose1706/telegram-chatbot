from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler
import os

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

# --- Cursos disponibles ---
CURSOS = {
    "curso1": "https://link-del-curso-1.com",
    "curso2": "https://link-del-curso-2.com",
    "curso3": "https://link-del-curso-3.com"
}

# --- Configuración del bot ---
bot_app = Application.builder().token(TOKEN).build()


async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Curso 1", callback_data="curso1")],
        [InlineKeyboardButton("Curso 2", callback_data="curso2")],
        [InlineKeyboardButton("Curso 3", callback_data="curso3")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 ¡Bienvenido! Selecciona un curso:", reply_markup=reply_markup)


async def button_click(update: Update, context):
    query = update.callback_query
    await query.answer()

    curso_id = query.data
    link = CURSOS.get(curso_id, "No existe el curso.")

    await query.edit_message_text(f"Aquí está el enlace del curso:\n\n{link}")


bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CallbackQueryHandler(button_click))


# --- Webhook ---
@app.post("/")
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    bot_app.update_queue.put_nowait(update)
    return "OK", 200


# Para correr en local si quieres
if __name__ == "__main__":
    bot_app.run_webhook(
        listen="0.0.0.0",
        port=5000,
        webhook_url="https://TU-APP.onrender.com"
    )
