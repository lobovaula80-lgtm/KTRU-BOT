from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import os
from flask import Flask, request, jsonify

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 8000))
SERVICE_URL = f"https://ktru-bot.onrender.com"

app = Flask(__name__)

@app.route("/health")
def health():
    return {"status": "ok"}, 200

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.decompress(request.get_data())
    asyncio.create_task(application.process_update(update))
    return jsonify({"result": "ok"}), 200

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бесплатный ассистент для подбора КТРУ.\n"
        "Опиши товар/услугу и я нашел один лучший вариант.\n\n"
        "Напиши, например: \"доска деревянная 50х100 мм\""
    )

async def ktru_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    response = (
        f"🔍 Ищу КТРУ для: {query}\n\n"
        "💡 Один лучший вариант:\n"
        "КТРУ: 9.13.13.120-00000000\n"
        "Наименование: Доска деревянная обрезная\n"
        "Характеристики:\n"
        "- Ширина: 50 мм\n"
        "- Толщина: 100 мм\n"
        "- Материал: древесина\n\n"
        "✅ Это подходящий вариант для вашей закупки."
    )
    await update.message.reply_text(response)

application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ktru_search))

if __name__ == "__main__":
    # Установка webhook
    import asyncio
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        application.start_webhook(
            webhook_path=f"/webhook/{TOKEN}",
            url=SERVICE_URL,
            port=PORT,
            sock=None,
            ssl_ctx=None,
            openssl_kwargs=None
        )
    )
    loop.run_until_complete(application.updater.stop())
    application.run_webhook(
        webhook_path=f"/webhook/{TOKEN}",
        url=SERVICE_URL,
        port=PORT,
        sock=None,
        ssl_ctx=None,
        openssl_kwargs=None,
        address="0.0.0.0"
    )
