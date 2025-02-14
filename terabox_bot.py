import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from flask import Flask, request

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a Flask application
app = Flask(__name__)

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

# Create a function to handle incoming updates from Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), updater.bot)
    updater.dispatcher.process_update(update)
    return 'ok'

# Initialize the bot
token = os.getenv("TELEGRAM_TOKEN")
updater = Updater(token)

# Register command handlers
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_terabox_link))

# Start the bot
updater.start_polling()

# WSGI entry point
if __name__ == '__main__':
    app.run(port=8443)