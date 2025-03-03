import logging
import io
import asyncio
from rembg import remove
from PIL import Image
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackContext

# إعداد التوكن
TOKEN = '*************** api'  # تأكد من وضع التوكن الصحيح

# إعداد نظام تسجيل الأخطاء
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,  # جعل مستوى التسجيل DEBUG لرؤية كل شيء
)

# دالة لمعالجة الصور وإزالة الخلفية
async def remove_background(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    logging.info(f"📸 تم استلام صورة من {chat_id}")

    if update.message.photo:
        photo_file = await update.message.photo[-1].get_file()
        photo_bytes = await photo_file.download_as_bytearray()

        logging.info("✅ تم تحميل الصورة، جاري إزالة الخلفية...")

        input_image = Image.open(io.BytesIO(photo_bytes))
        output_image = remove(input_image)

        bio = io.BytesIO()
        output_image.save(bio, format="PNG")
        bio.seek(0)

        await context.bot.send_photo(chat_id=chat_id, photo=bio)
        await update.message.reply_text("✅ تمت إزالة الخلفية! أرسل صورة أخرى إذا أردت.")
    else:
        await update.message.reply_text("❌ يرجى إرسال صورة!")

# دالة لبدء البوت
async def start(update: Update, context: CallbackContext):
    logging.info(f"🤖 مستخدم جديد: {update.message.chat_id}")
    await update.message.reply_text("👋 مرحبًا! أرسل لي صورة وسأزيل الخلفية لك.")

# الوظيفة الرئيسية لتشغيل البوت
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, remove_background))

    logging.info("🤖 البوت قيد التشغيل...")
    app.run_polling()

if __name__ == '__main__':
    main()
