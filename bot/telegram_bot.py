import os
import sys
import logging
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from telegram.constants import ChatAction
from core.image_processing import ImageProcessing

from transformers import pipeline
from telegram import Update
from telegram.ext import ContextTypes

# Initialize the emotion analysis pipeline
emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=False)


image_processor = ImageProcessing()

USER_DATA_FILE = 'user_data.json'

EMOTION_TO_EMOJI = {
    "joy": "😄",
    "anger": "😠",
    "sadness": "😢",
    "fear": "😨",
    "surprise": "😲",
    "neutral": "😐",
    "love": "❤️",
}

def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)



from transformers import pipeline
from telegram import Update
from telegram.ext import ContextTypes

# Initialize the emotion analysis pipeline
emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=False)

# Emoji mapping for emotions
EMOTION_TO_EMOJI = {
    "joy": "😄",
    "anger": "😠",
    "sadness": "😢",
    "fear": "😨",
    "surprise": "😲",
    "neutral": "😐",
    "love": "❤️",
}

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    # Notify the user that the bot is processing
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Analyze emotions
    emotion_result = emotion_analyzer(user_message)[0]
    detected_emotion = emotion_result["label"].lower()
    emoji = EMOTION_TO_EMOJI.get(detected_emotion, "🤔")  
    
    # Respond with the detected emotion and emoji
    response = f"I sense {detected_emotion} in your message. Here's an emoji for that: {emoji}"
    await update.message.reply_text(response)



async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    download_dir = "downloads"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    file_id = update.message.photo[-1].file_id
    file = await context.bot.get_file(file_id)
    file_path = os.path.join(download_dir, f"{file_id}.jpg")
    
    # Notify the user that the bot is processing the image
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    
    await file.download_to_drive(file_path)
   
    
    text = image_processor.extract_text_from_image(file_path)
    
    with open(file_path, 'rb') as img:
        await update.message.reply_photo(photo=img)
    
    await update.message.reply_text(text)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = update.message.voice.file_id
    file = await context.bot.get_file(file_id)
    
    # Notify the user that the bot is processing the voice note
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.RECORD_AUDIO)
    
    await file.download_to_drive(f"downloads/{file_id}.ogg")
    await update.message.reply_text("You sent a voice note. I've saved it!")


# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.application = ApplicationBuilder().token(self.token).build()

    def start_bot(self):
        from bot.handlers import start, help_command, unknown
        self.application.add_handler(CommandHandler("start", start))
        self.application.add_handler(CommandHandler("help", help_command))
        self.application.add_handler(MessageHandler(filters.COMMAND, unknown))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        self.application.add_handler(MessageHandler(filters.PHOTO, handle_image))
        self.application.add_handler(MessageHandler(filters.VOICE, handle_voice))
        self.application.run_polling()
