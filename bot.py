from flask import Flask, request
import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")  # Asegúrate de ponerlo en las variables de Render
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# --- HANDLERS DEL BOT ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        "¡Hola! 👋\nElige un curso:\n1️⃣ Desarrollo Web\n2️⃣ Marketing Digital\n3️⃣ Excel Básico"
    )

@bot.message_handler(func=lambda msg: True)
def handle_message(message):

    text = message.text.strip()

    if text == "1":
        bot.reply_to(message, "Aquí está tu curso de Desarrollo Web:\nhttps://t.me/+IIfD2Ud8W098YTc0")
    elif text == "2":
        bot.reply_to(message, "Curso de Marketing Digital:\nhttps://t.me/+abc123")
    elif text == "3":
        bot.reply_to(message, "Curso de Excel Básico:\nhttps://t.me/+xyz456")
    else:
        bot.reply_to(message, "Por favor envía 1, 2 o 3 😊")

# --- WEBHOOK ---
@app.route("/webhook", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def home():
    return "Bot funcionando correctamente", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv("WEBHOOK_URL"))
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
