import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# ------------------------------------
#  CONFIG
# ------------------------------------
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise Exception("No se encontró BOT_TOKEN en variables de entorno.")

CURSOS = {
    "curso1": "https://link-del-curso-1.com",
    "curso2": "https://link-del-curso-2.com",
    "curso3": "https://link-del-curso-3.com"
}

app = Flask(__name__)
tg_app = None


# ------------------------------------
# HANDLERS DEL BOT
# ------------------------------------
async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Curso 1", callback_data="curso1")],
        [InlineKeyboardButton("Curso 2", callback_data="curso2")],
        [InlineKeyboardButton("Curso 3", callback_data="curso3")]
    ]
    await update.message.reply_text(
        "👋 ¡Bienvenido! Selecciona un curso:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update, context):
    query = update.callback_query
    await query.answer()

    curso = query.data
    link = CURSOS.get(curso, "Curso no encontrado.")

    await query.edit_message_text(f"Aquí está el enlace del curso:\n\n{link}")


# ------------------------------------
# WEBHOOK RECEIVER
# ------------------------------------
@app.post("/")
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, tg_app.bot)
    tg_app.update_queue.put_nowait(update)
    return "OK", 200


# ------------------------------------
# INICIALIZACIÓN DEL BOT
# ------------------------------------
async def setup_bot():
    global tg_app
    tg_app = Application.builder().token(TOKEN).build()

    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(CallbackQueryHandler(button))

    await tg_app.initialize()
    await tg_app.start()


# ------------------------------------
# ARRANQUE DE FLASK + BOT
# ------------------------------------
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_bot())

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
