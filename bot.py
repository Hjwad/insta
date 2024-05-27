import os
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
from dotenv import load_dotenv
import instaloader
import telebot

# Load environment variables from .env file
load_dotenv()

# Instagram API credentials
INSTAGRAM_API_ID = os.getenv('INSTAGRAM_API_ID')
INSTAGRAM_API_SECRET = os.getenv('INSTAGRAM_API_SECRET')

# Bot token
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Initialize Instaloader
L = instaloader.Instaloader()

def download_instagram_post(url):
    try:
        post_shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, post_shortcode)
        download_path = f"./downloads/{post.owner_username}"
        os.makedirs(download_path, exist_ok=True)
        L.download_post(post, target=download_path)
        files = os.listdir(download_path)
        if files:
            return download_path, files
        else:
            return download_path, []
    except instaloader.exceptions.BadResponseException as e:
        return None, f"حدث خطأ أثناء التحميل: قد يكون الرابط غير صالح أو قد تحتاج لتسجيل الدخول."
    except Exception as e:
        return None, f"حدث خطأ أثناء التحميل: {str(e)}"

# Initialize Telegram bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً! أرسل رابط Instagram لتحميل المحتوى.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    download_path, response = download_instagram_post(url)
    if download_path:
        for file in response:
            file_path = os.path.join(download_path, file)
            with open(file_path, 'rb') as f:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    bot.send_photo(message.chat.id, f)
                elif file.lower().endswith('.mp4'):
                    bot.send_video(message.chat.id, f)
                else:
                    bot.send_document(message.chat.id, f)
        # Delete files after uploading
        for file in response:
            os.remove(os.path.join(download_path, file))
        os.rmdir(download_path)
    else:
        bot.reply_to(message, response)

# Start polling
bot.polling()
