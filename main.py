import os
import requests
import time
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ==================== خادم وهمي لـ Render ====================
# Render يحتاج لسيرفر يعمل على منفذ PORT لإبقاء البوت شغالاً
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running successfully!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)
# ============================================================

# جلب التوكنات من إعدادات Render الأمنية
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
HUGGINGFACE_API_TOKEN = os.environ.get("HUGGINGFACE_API_TOKEN")

MODEL_URL = "https://api-inference.huggingface.co/models/damo-vilab/text-to-video-ms-1.7b"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

# أمر البداية /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "أهلاً بك! 👋\n"
        "أنا بوت صناعة الفيديوهات بالذكاء الاصطناعي.\n\n"
        "أرسل لي وصفاً للفيديو الذي تريده باللغة الإنجليزية وسأقوم بتوليده لك مجاناً!\n"
        "مثال: A running horse in a beautiful forest, cinematic"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

# دالة توليد الفيديو
async def generate_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    status_msg = await update.message.reply_text("⏳ جاري معالجة الطلب وصناعة الفيديو... قد يستغرق هذا من 1 إلى 3 دقائق، يرجى الانتظار.")

    payload = {"inputs": prompt}

    try:
        response = requests.post(MODEL_URL, headers=HEADERS, json=payload, timeout=300)

        if response.status_code == 503:
            await status_msg.edit_text("🔄 النموذج يتم تحميله حالياً في السيرفر، جاري المحاولة مرة أخرى خلال 20 ثانية...")
            time.sleep(20)
            response = requests.post(MODEL_URL, headers=HEADERS, json=payload, timeout=300)

        if response.status_code == 200:
            video_path = "generated_video.mp4"
            with open(video_path, "wb") as f:
                f.write(response.content)

            await status_msg.edit_text("✅ تم إنشاء الفيديو بنجاح! جاري الإرسال...")
            with open(video_path, "rb") as video_file:
                await update.message.reply_video(video=video_file, caption=f"🎬 الوصف: {prompt}")

            if os.path.exists(video_path):
                os.remove(video_path)
        else:
            await status_msg.edit_text(f"❌ حدث خطأ أثناء التوليد. (رمز الخطأ: {response.status_code})")

    except Exception as e:
        await status_msg.edit_text(f"❌ حدث خطأ: {str(e)}")

# التشغيل الرئيسي
if __name__ == "__main__":
    # تشغيل السيرفر الوهمي في الخلفية
    Thread(target=run_flask).start()

    # تشغيل بوت تلغرام
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_video))

    print("🤖 البوت يعمل على Render...")
    app.run_polling()
```
