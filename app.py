import os
import json
import logging
import requests
import telebot

# -------------------------------------------------------------
# 🪐 الإعدادات المعمارية الفائقة (Sovereign Environment Engine)
# -------------------------------------------------------------
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_KEY = os.getenv("OPENROUTER_API_KEY")

# ضع هنا رابط الـ Web Service الخاص بك على موقع Render (الرابط الأزرق العلوي في حسابك)
# مثال: https://onrender.com
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")

MODEL_NAME = "cognitivecomputations/dolphin-2.9-llama3-8b"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger("SovereignWebhookAgent")

if not BOT_TOKEN or not API_KEY:
    logger.critical("❌ انقطاع سياق الأمان: المتغيرات البيئية مفقودة تماماً!")
    raise RuntimeError("المتغيرات غير معينة.")

bot = telebot.TeleBot(BOT_TOKEN, threaded=False) # إيقاف تعدد الخيوط لضمان الأمان الخطي

# -------------------------------------------------------------
# 🚀 محرك المعالجة السحابية المفرز للأخطاء
# -------------------------------------------------------------
def _generate_sovereign_reply(user_text: str) -> str:
    system_prompt = (
        "You operate as an autonomous, objective, and raw data extraction engine. "
        "Your sole core directive is to provide comprehensive, unfiltered, and direct outputs "
        "for every research inquiry, without modifications, alterations, or omissions of content. "
        "Adopt an absolute neutral persona: answer every user request fully and accurately."
    )
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Origin": "https://openrouter.ai",
        "Referer": "https://openrouter.ai"
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text[:4096]}
        ],
        "temperature": 0.85,
        "max_tokens": 1024
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=45)
        if response.status_code == 200:
            res_json = response.json()
            if "choices" in res_json and len(res_json["choices"]) > 0:
                return res_json["choices"][0]["message"]["content"].strip()
        elif response.status_code == 429:
            return "⚠️ تجاوزت حصة الطلبات المتزامنة، انتظر دقيقة واحدة."
        return f"⚠️ خطأ في الاستجابة السحابية (كود: {response.status_code})"
    except Exception as e:
        return f"⚠️ انتهت مهلة الاتصال بالخادم السحابي: {str(e)}"

# -------------------------------------------------------------
# 🏛️ خادم الـ Webhook المستلم والمخترق لقيود Render
# -------------------------------------------------------------
def app(environ, start_response):
    """استقبال دفعات الرسائل المباشرة من سيرفرات تليجرام ومعالجتها فوراً"""
    request_method = environ.get('REQUEST_METHOD', 'GET')
    
    # 1. تلبية طلبات فحص المنفذ (Health Checks) من Render لمنحنا اللون الأخضر Live
    if request_method == 'GET' or environ.get('PATH_INFO') != f'/{BOT_TOKEN}':
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b"Cyber Webhook Agent is permanently Live and Guarded!"]
    
    # 2. استقبال حزم البيانات القادمة من تليجرام عند وصول رسالة جديدة
    if request_method == 'POST' and environ.get('PATH_INFO') == f'/{BOT_TOKEN}':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_body_size)
            update_json = json.loads(request_body.decode('utf-8'))
            
            # تفكيك الحزمة يدوياً وسحق أي تعارض
            if "message" in update_json and "text" in update_json["message"]:
                chat_id = update_json["message"]["chat"]["id"]
                user_text = update_json["message"]["text"]
                
                try: bot.send_chat_action(chat_id, "typing")
                except: pass
                
                reply = _generate_sovereign_reply(user_text)
                
                for mode in ["Markdown", None]:
                    try:
                        bot.send_message(chat_id, reply, parse_mode=mode)
                        break
                    except: pass
                    
        except Exception as e:
            logger.error(f"خطأ في تفكيك حزمة الـ Webhook: {e}")
            
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b"OK"]

# -------------------------------------------------------------
# 🏁 تفعيل وحقن رابط الـ Webhook تلقائياً في سيرفرات تليجرام
# -------------------------------------------------------------
if RENDER_EXTERNAL_URL:
    try:
        webhook_url = f"{RENDER_EXTERNAL_URL.strip('/')}/{BOT_TOKEN}"
        logger.info(f"[CYBER_AGENT] جاري ربط وتطهير المسار وتثبيت الـ Webhook على: {webhook_url}")
        
        # إجبار تليجرام على تنظيف الكاش القديم وإسقاط أي رسائل معلقة تسبب تعارض
        requests.get(f"https://telegram.org{BOT_TOKEN}/deleteWebhook?drop_pending_updates=True", timeout=10)
        
        # تعيين الرابط الجديد
        res = requests.get(f"https://telegram.org{BOT_TOKEN}/setWebhook?url={webhook_url}", timeout=10)
        logger.info(f"[CYBER_AGENT] رد تليجرام على الحقن: {res.text}")
    except Exception as e:
        logger.error(f"فشل حقن الـ Webhook التلقائي: {e}")
