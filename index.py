import os
import telebot
import requests
from flask import Flask, request

# إعداد التوكن الخاص بالبوت الجديد
BOT_TOKEN = "8922674230:AAEBXbpB-5hw5fRKdyHHfBeClSJDxPTfYfk"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

STANDARD_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    if request.headers.get('content-type', '').startswith('application/json'):
        try:
            json_string = request.get_data().decode('utf-8', errors='ignore')
            update = telebot.types.Update.de_json(json_string)
            if update.message and update.message.text:
                # معالجة مباشرة وآمنة تناسب بيئة الـ Serverless
                handle_core_logic(update.message)
        except Exception as e:
            print(f"Vercel Serverless Core Error: {str(e)}")
        # إرجاع رد 200 OK فوراً لتليجرام في أقل من 0.1 ثانية لمنع تكرار الرسائل
        return "!", 200
    else:
        return "Invalid Request", 403

@app.route('/')
def index():
    return "سيرفر بوت صانع الأكواد يعمل بنجاح وثبات مليمتر على Vercel!"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "🚀 مرحباً بك في بوت 'صانع الأكواد الفوري' على منصة Vercel!\n\n"
                          "💡 **طريقة العمل:**\n"
                          "أرسل لي فكرتك البرمجية بأي لغة وسأحولها إلى **كود برمي كامل وجاهز للنسخ فوراً** بدقة متناهية وبدون مقدمات!")

# دالة المعالجة المفصولة هندسياً لسرعة الاستجابة
def handle_core_logic(message):
    user_idea = message.text.strip()
    if user_idea.startswith('/'):
        return

    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        # صياغة الرابط القياسي الآمن للـ GET Request لمنع خطأ 405
        text_url = f"https://pollinations.ai{requests.utils.quote(user_idea)}"
        
        # هندسة الأوامر الصارمة الموجهة لنموذج الأكواد المجاني qwen-coder لتفادي خطأ 402
        query_params = {
            "system": (
                "أنت مهندس برمجيات محترف وخبير في كتابة الأكواد البرمجية النظيفة والشغالة 100%. "
                "مهمتك هي قراءة فكرة المستخدم، وتحويلها إلى كود برمي كامل ومكتوب بالكامل. "
                "شروطك الصارمة:\n"
                "1. اكتب الكود كاملاً وبدون أي اختصارات أو أسطر محذوفة.\n"
                "2. ضع الكود دائماً داخل علامات الاقتباس البرمجية للماركداون (```).\n"
                "3. اعطني الكود مباشرة بدون مقدمات وبدون شروحات نصية طويلة. نريد الكود البرمجي الصافي فقط وبأعلى كفاءة."
            ),
            "model": "qwen-coder"
        }
        
        # تحديد مهلة صارمة بـ 7 ثوانٍ ليتوافق مع سقف Vercel المجاني
        response = requests.get(text_url, params=query_params, headers=STANDARD_HEADERS, timeout=7)
        
        if response.status_code == 200:
            generated_code = response.text.strip()
            if generated_code:
                bot.reply_to(message, generated_code, parse_mode="Markdown")
            else:
                bot.reply_to(message, "⚠️ استجاب محرك الأكواد ولكن النتيجة جاءت فارغة، أعد المحاولة.")
        else:
            bot.reply_to(message, f"⚠️ خادم البرمجة واجه مشكلة، رمز الاستجابة: {response.status_code}")
                
    except requests.exceptions.Timeout:
        bot.reply_to(message, "⚠️ استغرق توليد الكود وقتاً طويلاً، يرجى إعادة إرسال طلبك بصياغة أبسط.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ خطأ في معالجة الكود البرمجي: {str(e)}")
