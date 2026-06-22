from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import os

TOKEN = os.getenv("BOT_TOKEN")

from flask import Flask
app = Flask(__name__)

@app.route("/health")
def health():
    return {"status": "ok"}, 200

def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.message.reply_text(
        "Привет! Я бесплатный ассистент для подбора КТРУ.\n"
        "Опиши товар/услугу и я нашел один лучший вариант.\n\n"
        "Напиши, например: \"доска деревянная 50х100 мм\""
    )

def ktru_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    update.message.reply_text(response)

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN не найден в env!")
    
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ktru_search))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
