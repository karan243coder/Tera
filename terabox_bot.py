import os
import logging
import requests
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

# Function to get configuration
def get_config():
    response = requests.get("https://teradl-api.dapuntaratya.com/get_config")
    return response.json()

# Function to generate file
def generate_file(mode, url):
    response = requests.post("https://teradl-api.dapuntaratya.com/generate_file", data={"mode": mode, "url": url})
    return response.json()

# Function to generate link
def generate_link(mode, js_token, cookie, sign, timestamp, shareid, uk, fs_id):
    response = requests.post("https://teradl-api.dapuntaratya.com/generate_link", data={
        "mode": mode,
        "js_token": js_token,
        "cookie": cookie,
        "sign": sign,
        "timestamp": timestamp,
        "shareid": shareid,
        "uk": uk,
        "fs_id": fs_id
    })
    return response.json()

# Define a function to handle text messages (TeraBox links)
async def handle_terabox_link(update: Update, context: CallbackContext) -> None:
    terabox_link = update.message.text

    if "terabox" in terabox_link:
        # Example of using the API
        config = get_config()
        if config['status'] == 'success':
            mode = config['service'][0]['params'][0]  # Example: get mode from config
            file_response = generate_file(mode, terabox_link)
            if file_response['status'] == 'success':
                # Process the response and send a message back
                await update.message.reply_text(f"File generated successfully: {file_response}")
            else:
                await update.message.reply_text("Failed to generate file.")
        else:
            await update.message.reply_text("Failed to get configuration.")
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