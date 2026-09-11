import os
import sys
import io
import contextlib
import telebot

# 1. ضع التوكن الخاص بك هنا أو اتركه ليجلب تلقائياً من السيرفر
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8810608330:AAG3ZZnLgi7Jyyx4vqrxk7xfqzXGdBO5Mec')
bot = telebot.TeleBot(BOT_TOKEN)

# 2. ضع معرف الـ ID الخاص بحسابك أنت فقط (يتكون من أرقام فقط)
# يمكنك معرفة الـ ID الخاص بك عبر إرسال رسالة للبوت الرسمي @userinfobot
OWNER_ID = 6955055370  # استبدل هذا الرقم بـ ID حسابك الحقيقي

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك يا مطوري. أنا جاهز لتنفيذ أوامرك المطلقة.")

@bot.message_handler(func=lambda message: True)
def execute_code(message):
    # التحقق من أن الشخص الذي يرسل الأمر هو صاحب البوت حصراً
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ عذراً، هذا البوت مخصص للمطور الخاص به فقط.")
        return

    # استقبال النص ككود بايثون وتجهيز بيئة لتنفيذه
    code = message.text
    
    # لإنشاء واجهة برمجية لالتقاط المخرجات (الأخطاء أو النصوص المطبوعة)
    output = io.StringIO()
    
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        # تنفيذ الكود والتقاط المخرجات
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            # إعداد البيئة لتنفيذ الأكواد المتعددة الأسطر
            exec_globals = {"bot": bot, "message": message, "telebot": telebot, "os": os, "sys": sys}
            exec(code, exec_globals)
            
        result = output.getvalue()
        if not result:
            result = "✅ تم تنفيذ الأمر بنجاح (بدون مخرجات نصية)."
            
    except Exception as e:
        # في حال حدوث خطأ برمجي في الكود الذي أرسلته
        result = f"❌ حدث خطأ أثناء التنفيذ:\n`{str(e)}`"

    # إرسال النتيجة للمطور
    # إذا كانت النتيجة طويلة جداً، يتم قصها لكي لا تفشل عملية الإرسال في تليجرام
    if len(result) > 4000:
        bot.reply_to(message, result[:4000] + "\n... النتيجة طويلة جداً تم قصها.")
    else:
        bot.reply_to(message, result, parse_mode="Markdown" if "❌" in result else None)

# تشغيل البوت 24/7
bot.infinity_polling()
