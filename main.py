import os
import sys
import curses
import time
# Add the 'bot' module to the path if necessary
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'bot')))

from bot.telegram_bot import TelegramBot
from bot.config import BOT_TOKEN

def run_aurora_ui(stdscr):
    # Hide the cursor
    curses.curs_set(0)

    # Set up color pairs for a cool UI
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Clear screen and create a welcoming interface
    stdscr.clear()
    stdscr.refresh()

    # Title Animation (welcome text)
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(2, 10, "Welcome to Aurora's Brain Interface!", curses.A_BOLD)
    stdscr.attroff(curses.color_pair(1))

    # Wait for a moment and animate
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(4, 10, "Initializing Aurora...", curses.A_BOLD)
    stdscr.attroff(curses.color_pair(2))
    stdscr.refresh()
    time.sleep(2)

    # Display a cool ASCII Art (or any custom intro)
    intro_text = """
         ____                              
        |  _ \  ___  ___   __ _ _ __  __ _ _ __ 
        | |_) |/ _ \/ _ \ / _` | '_ \/ _` | '_ \ 
        |  __/|  __/ (_) | (_| | | | | (_| | | | |
        |_|    \___|\___/ \__,_|_| |_|\__,_|_| |_|
    """
    stdscr.addstr(6, 10, intro_text)
    stdscr.refresh()

    # Wait a little before transitioning to bot
    time.sleep(3)

    # Now we start the actual bot
    stdscr.clear()
    stdscr.addstr(10, 10, "Aurora is now online... Press 'Ctrl+C' to exit.", curses.A_BOLD)
    stdscr.refresh()
    time.sleep(1)

    start_aurora()

  


def start_aurora():
    # Initialize the bot
    bot = TelegramBot(BOT_TOKEN)
    
    # Start the bot
    bot.start_bot()

if __name__ == '__main__':
 
    curses.wrapper(run_aurora_ui)
