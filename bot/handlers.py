# bot/handlers.py

from telegram import Update
from telegram.ext import CallbackContext
import openai
import os

from bot.config import Aurora_OpenAI_key

openai.api_key = Aurora_OpenAI_key

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

async def generate_gpt_response(prompt: str) -> str:
    try:
        response = await openai.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {"role": "system", "content": "You are a helpful assistant, a friendly friend named Aurora with the nickname Rori, built by Donald Mxolisi."},
                {"role": "user", "content": prompt},
            ],
        )
        return response['choices'][0]['message']['content'].strip()
    
    except Exception as e:
        print(f"Error generating GPT response: {e}")
        return "Sorry, I couldn't generate a response right now."
