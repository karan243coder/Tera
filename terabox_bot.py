import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from flask import Flask, request

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a Flask application
app = Flask(__name__)

# Initialize the bot
token = "7400491029:AAF5r3cfKWpP8aXjI683z3izeca1YLhGVXc"  # Replace with your actual token
application = ApplicationBuilder().token(token).build()

# Define a command handler for the /start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Welcome! Send me a TeraBox link to stream the video.')

# Define a function to handle text messages (TeraBox links)
async def handle_terabox_link(update: Update, context: CallbackContext) -> None:
    terabox_link = update.message.text

    if "terabox" in terabox_link:
        video_player_link = f"https://bimbo69.netlify.app/?link={terabox_link}"
        await update.message.reply_text(f'You can watch your video here: {video_player_link}')
    else:
        await update.message.reply_text('Please send a valid TeraBox link.')

# Create a function to handle incoming updates from Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.dispatcher.process_update(update)
    return 'ok'

# Register command handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_terabox_link))

# WSGI entry point
if __name__ == '__main__':
    app.run(port=8443)