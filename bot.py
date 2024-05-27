import os
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
from dotenv import load_dotenv
pip freeze > requirements.txt
# تحميل المتغيرات من ملف .env
load_dotenv()

# معرف التطبيق ورمز العميل الخاصين بتطبيق Instagram
INSTAGRAM_APP_ID = os.getenv('INSTAGRAM_APP_ID')
INSTAGRAM_APP_SECRET = os.getenv('INSTAGRAM_APP_SECRET')

# تعويض هنا بمعرف البوت الخاص بك
BOT_TOKEN = os.getenv('BOT_TOKEN')

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="مرحبا! أرسل اسم مستخدم Instagram لبدء التحميل.")

def download_instagram_posts(username):
    access_token = get_access_token()
    if access_token:
        url = f'https://graph.instagram.com/v12.0/{username}/media?access_token={access_token}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for post in data['data']:
                media_url = post['media_url']
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=media_url)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="حدث خطأ أثناء التحميل.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="حدث خطأ في المصادقة.")

def get_access_token():
    url = f'https://graph.instagram.com/oauth/access_token?client_id={INSTAGRAM_APP_ID}&client_secret={INSTAGRAM_APP_SECRET}&grant_type=client_credentials'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['access_token']
    else:
        return None

def instagram(update, context):
    username = context.args[0]
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    download_instagram_posts(username)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="آسف، لا أفهم هذا الأمر.")

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("instagram", instagram))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
