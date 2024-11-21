# bot/handlers.py

from telegram import Update
from telegram.ext import CallbackContext
import openai
import os


async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"Hi {user}! 😊 I'm Aurora, your personal forex assistant. Let's conquer the markets together!"
    )

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "I'm here to help! Here's what I can do:\n"
        "- /start: Introduce myself\n"
        "- /trade: Discuss trading strategies\n"
        "- /balance: Check your trading account balance\n"
        "- /news: Get the latest forex news\n"
        "Just type a command, and I'll assist!"
    )

async def unknown(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Oops, I didn't understand that command. 😅 Try /help to see what I can do!"
    )

