import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# جلب توكن البوت من المتغيرات البيئية في Vercel
TOKEN = os.environ.get("8810608330:AAG3ZZnLgi7Jyyx4vqrxk7xfqzXGdBO5Mec")
TELEGRAM_API_URL = f"https://telegram.org{TOKEN}/sendMessage"

def send_message(chat_id, text):
    """دالة بسيطة ومباشرة لإرسال الرسائل عبر تلقرام"""
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        response = requests.post(TELEGRAM_API_URL, json=payload)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        data = request.get_json(force=True)
        
        # التأكد من أن البيانات تحتوي على رسالة نصية قادمة من مستخدم
        if "message" in data and "text" in data["message"]:
            chat_id = data["message"]["chat"]["id"]
            user_text = data["message"]["text"]
            
            # إذا أرسل المستخدم أمر البداية
            if user_text == "/start":
                reply = "أهلاً بك! أنا جاهز لتنفيذ طلباتك. ماذا تريد مني أن أفعل؟"
            else:
                # --- [ضع هنا منطق البوت الخاص بك مستقبلاً] ---
                reply = f"لقد استلمت طلبك: {user_text}\n(يمكنك لاحقاً ربط هذا الجزء بأي ذكاء اصطناعي تريد)."
            
            # إرسال الرد للمستخدم فوراً
            send_message(chat_id, reply)
            
        return jsonify({"status": "success"}), 200
    return "OK", 200

@app.route('/')
def home():
    return "البوت يعمل بنجاح وبأعلى كفاءة على Vercel!", 200
