import telebot
import instaloader
import os

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

L = instaloader.Instaloader()

def download_instagram_post(url):
    try:
        post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
        L.download_post(post, target=f"./downloads/{post.owner_username}")
        return f"تم تحميل البوست من المستخدم {post.owner_username}."
    except Exception as e:
        return f"حدث خطأ أثناء التحميل: {str(e)}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً! أرسل رابط Instagram لتحميل المحتوى.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    response = download_instagram_post(url)
    bot.reply_to(message, response)

bot.polling()
