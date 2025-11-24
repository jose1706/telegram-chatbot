import logging
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import config

# --------------------- CONFIG ---------------------
TOKEN = config.TOKEN
WEBHOOK_URL = config.WEBHOOK_URL

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# --------------------- BOT ---------------------
application = Application.builder().token(TOKEN).build()


# --------------------- HOME ---------------------
@app.get("/")
def home():
    return "Bot funcionando correctamente (Render despierto)."


# --------------------- HANDLERS ---------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📘 Habilidades Digitales", callback_data="curso1")],
        [InlineKeyboardButton("🚀 Emprendimiento", callback_data="curso2")],
        [InlineKeyboardButton("📣 Marketing Digital", callback_data="curso3")],
        [InlineKeyboardButton("📝 Mi progreso", callback_data="progreso")]
    ]

    await update.message.reply_text(
        "👋 *¡Bienvenido al programa de formación de la Comuna 6!* \n\n"
        "Selecciona un curso:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user_name = query.from_user.first_name

    context.bot_data.setdefault("usuarios", {})[user_id] = {"nombre": user_name}

    if query.data == "curso1":
        await query.edit_message_text(
            "📘 *Curso 1 – Habilidades Digitales*\n\nContenido:\n👉 https://t.me/+TU_CANAL_1",
            parse_mode="Markdown"
        )

    elif query.data == "curso2":
        await query.edit_message_text(
            "🚀 *Curso 2 – Emprendimiento*\n\nContenido:\n👉 https://t.me/+TU_CANAL_2",
            parse_mode="Markdown"
        )

    elif query.data == "curso3":
        await query.edit_message_text(
            "📣 *Curso 3 – Marketing Digital*\n\nContenido:\n👉 https://t.me/+TU_CANAL_3",
            parse_mode="Markdown"
        )

    elif query.data == "progreso":
        progreso = context.bot_data.get("progreso", {})
        cursos_usuario = progreso.get(user_id, [])
        texto = (
            "Aún no has completado ningún curso."
            if not cursos_usuario
            else "🏅 *Cursos completados:*\n" + "\n".join([f"✔ {c}" for c in cursos_usuario])
        )
        await query.edit_message_text(texto, parse_mode="Markdown")


async def registrar_progreso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message.text.lower()
    user_id = update.message.from_user.id

    if mensaje.startswith("terminé curso"):
        curso = mensaje.replace("terminé curso", "").strip()
        progreso = context.bot_data.setdefault("progreso", {})
        progreso.setdefault(user_id, []).append(curso)

        await update.message.reply_text(
            f"🎉 ¡Excelente! Registré que finalizaste el curso *{curso}*!",
            parse_mode="Markdown"
        )


# ------------------ WEBHOOK ---------------------
@app.post("/webhook")
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)

    # INVOCAMOS LA FUNCIÓN ASYNC CORRECTAMENTE
    asyncio.create_task(application.process_update(update))

    return "ok"


@app.get("/setwebhook")
def set_webhook():
    asyncio.run(application.bot.set_webhook(url=WEBHOOK_URL))
    return f"Webhook configurado en {WEBHOOK_URL}"


# ------------------ START ---------------------
if __name__ == "__main__":
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(buttons))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, registrar_progreso))

    print("Bot en ejecución con webhook…")
    app.run(host="0.0.0.0", port=10000)
