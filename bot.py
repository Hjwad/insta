import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import instaloader

# استبدل هذا بالتوكن الخاص بك
API_TOKEN = '6657123307:AAGxcxRf5XXElbE93JesIqpp2ijp-9ltkGc'

# إعداد instaloader
L = instaloader.Instaloader()

# دالة لبدء البوت
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('مرحباً! أرسل لي رابط منشور على إنستجرام لتحميل الوسائط.')

# دالة لتحميل الوسائط من إنستجرام
def download_instagram_media(update: Update, context: CallbackContext) -> None:
    url = update.message.text.strip()
    try:
        post = instaloader.Post.from_shortcode(L.context, url.split('/')[-2])
        L.download_post(post, target='downloads')
        
        for file_name in os.listdir('downloads'):
            if file_name.endswith(('.jpg', '.mp4')):
                file_path = os.path.join('downloads', file_name)
                update.message.reply_document(document=open(file_path, 'rb'))
                os.remove(file_path)

    except Exception as e:
        update.message.reply_text(f'حدث خطأ: {e}')
    finally:
        for file_name in os.listdir('downloads'):
            os.remove(os.path.join('downloads', file_name))

def main():
    # إعداد الـ Updater مع التوكن
    updater = Updater(API_TOKEN, use_context=True)

    # الحصول على الموزع (Dispatcher) لتسجيل المعالجات (Handlers)
    dp = updater.dispatcher

    # تسجيل معالج الأوامر /start
    dp.add_handler(CommandHandler("start", start))

    # تسجيل معالج الروابط النصية من إنستجرام
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_instagram_media))

    # بدء البوت
    updater.start_polling()

    # جعل البوت يعمل حتى يتم إيقافه يدوياً
    updater.idle()

if __name__ == '__main__':
    # إنشاء مجلد لتحميل الملفات إذا لم يكن موجوداً
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    main()
