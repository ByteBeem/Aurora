import os
import sys

# Add the 'bot' module to the path if necessary
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'bot')))

from bot.telegram_bot import TelegramBot
from bot.config import BOT_TOKEN


def main():
    # Initialize the bot
    bot = TelegramBot(BOT_TOKEN)
    
    # Start the bot
    bot.start_bot()

if __name__ == "__main__":
    main()
