import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a command handler for the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Send me a TeraBox link to stream the video.')

# Define a function to handle text messages (TeraBox links)
def handle_terabox_link(update: Update, context: CallbackContext) -> None:
    terabox_link = update.message.text

    if "terabox" in terabox_link:
        video_player_link = f"https://bimbo69.netlify.app/?link={terabox_link}"
        update.message.reply_text(f'You can watch your video here: {video_player_link}')
    else:
        update.message.reply_text('Please send a valid TeraBox link.')

def main() -> None:
    # Get the bot token from the environment variable
    token = os.getenv("TELEGRAM_TOKEN")
    updater = Updater(token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_terabox_link))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
