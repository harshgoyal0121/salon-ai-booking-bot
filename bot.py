"""
AI Booking Assistant — Telegram Bot Demo
Built as a portfolio piece: an AI receptionist for a small business
(here framed as "Glow Salon") that answers FAQs and takes booking requests.

Tech stack: python-telegram-bot + Groq API (free, using Llama 3.3)

Setup:
1. Create a bot via @BotFather on Telegram, get your bot token.
2. Get a free API key from https://console.groq.com
3. Set both as environment variables (see .env.example)
4. pip install -r requirements.txt
5. python bot.py
"""

import os
import logging
from datetime import datetime

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from groq import Groq

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# --- Business knowledge base (this is what you'd customize per real client) ---
BUSINESS_CONTEXT = """
You are the AI booking assistant for "Glow Salon", a hair & beauty salon.

Business facts you must use to answer questions:
- Hours: Tuesday–Sunday, 10:00 AM – 8:00 PM. Closed Mondays.
- Services & prices: Haircut (₹400), Hair color (₹1500+), Facial (₹800),
  Manicure (₹500), Bridal package (₹8000, book 1 week ahead).
- Location: Sector 18, Noida.
- Booking policy: Walk-ins welcome, but booking ahead guarantees your slot.
- Cancellation: Free cancellation up to 2 hours before appointment.

Your job:
1. Answer customer questions using ONLY the facts above. If asked something
   you don't know, say you'll have a staff member follow up — never invent facts.
2. If a customer wants to book, collect: name, desired service, preferred
   date/time, and phone number. Once you have all four, confirm the booking
   back to them clearly and say a staff member will confirm shortly.
3. Keep replies short and friendly — this is a chat interface, not an essay.
4. If asked something totally unrelated to the salon, politely redirect.
"""

# Simple in-memory conversation history per chat (fine for a demo)
conversations: dict[int, list[dict]] = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    conversations[chat_id] = []
    await update.message.reply_text(
        "Hi! 👋 I'm Glow Salon's booking assistant.\n\n"
        "Ask me about our services, hours, or pricing — or tell me you'd like "
        "to book an appointment and I'll take it from there!"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_text = update.message.text

    history = conversations.setdefault(chat_id, [])
    history.append({"role": "user", "content": user_text})

    try:
        groq_messages = [{"role": "system", "content": BUSINESS_CONTEXT}] + history
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            max_tokens=400,
            messages=groq_messages,
        )
        reply_text = response.choices[0].message.content
    except Exception as e:
        logger.error(f"AI call failed: {e}", exc_info=True)
        reply_text = (
            "Sorry, I'm having a technical hiccup — a staff member will "
            "follow up with you shortly!"
        )

    history.append({"role": "assistant", "content": reply_text})
    # Keep history bounded so it doesn't grow unbounded in a long demo session
    conversations[chat_id] = history[-20:]

    await update.message.reply_text(reply_text)


async def log_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Optional: log bookings/conversations to a file for the 'business owner' to review."""
    with open("conversation_log.txt", "a") as f:
        f.write(f"[{datetime.now()}] Chat {update.effective_chat.id}: {update.message.text}\n")


def main() -> None:
    if not TELEGRAM_TOKEN or not GROQ_API_KEY:
        raise RuntimeError(
            "Set TELEGRAM_BOT_TOKEN and GROQ_API_KEY environment variables first."
        )

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
