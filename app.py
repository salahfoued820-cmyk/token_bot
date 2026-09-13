import streamlit as st
import requests
from bs4 import BeautifulSoup

# إعدادات الصفحة البرمجية لـ Streamlit
st.set_page_config(page_title="منصة صلاح للترجمة الذكية", page_icon="🌐", layout="centered")

# واجهة الموقع والعناوين
st.title("🌐 منصة صلاح العالمية للترجمة الذكية")
st.write("ترجمة النصوص والصور فوراً بأحدث التقنيات السحابية المحصنة مجاناً 🚀")

# قائمة اللغات المتاحة مع أسمائها الرسمية لمحرك البحث
LANGUAGES = {
    "العربية": "Arabic",
    "الإنجليزية (English)": "English",
    "الفرنسية (Français)": "French",
    "الألمانية (Deutsch)": "German",
    "الإيطالية (Italiano)": "Italian",
    "الإسبانية (Español)": "Spanish"
}

# قائمة منسدلة تفاعلية لاختيار اللغة
target_lang_name = st.selectbox("🎯 اختر اللغة التي تريد الترجمة إليها:", list(LANGUAGES.keys()))
target_lang_text = LANGUAGES[target_lang_name]

# إنشاء تبويبات لفصل نظام النصوص عن الصور
tab1, tab2 = st.tabs(["📝 ترجمة النصوص", "📸 ترجمة الصور"])

def fetch_translation(text_to_translate, target_language):
    """دالة محصنة ومستقرة للترجمة الفورية عبر خادم DuckDuckGo"""
    try:
        url = "https://duckduckgo.com"
        full_prompt = f"Translate the following text into {target_language}. Give me only the translated text without any introduction or additional words: {text_to_translate}"
        payload = {'q': full_prompt}
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        
        response = requests.post(url, data=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = [a.text for a in soup.find_all('a', class_='result__snippet')]
            if results:
                return results[0].strip()
        return None
    except Exception:
        return None

with tab1:
    user_text = st.text_area("✏️ اكتب أو الصق النص المراد ترجمته هنا:", placeholder="Hello my friend...", key="input_text")
    if st.button("🔄 ترجم النص الآن", key="btn_text"):
        if user_text.strip():
            with st.spinner("جاري معالجة الترجمة..."):
                translated_text = fetch_translation(user_text, target_lang_text)
                if translated_text:
                    st.success("✨ **الترجمة الاحترافية المعتمدة:**")
                    st.info(translated_text)
                else:
                    st.error("⚠️ خادم الترجمة يواجه ضغطاً مؤقتاً حالياً، يرجى إعادة الضغط على الزر للمحاولة مجدداً.")
        else:
            st.warning("⚠️ من فضلك، اكتب نصاً أولاً قبل الضغط على زر الترجمة.")

with tab2:
    uploaded_file = st.file_uploader("📥 اسحب وأسقط صورة تحتوي على كتابة هنا:", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="📸 الصورة المرفوعة بنجاح", use_column_width=True)
        
        if st.button("🔍 اقرأ وترجم الصورة فوراً", key="btn_img"):
            with st.spinner("جاري قراءة الصورة واستخراج النصوص سحابياً..."):
                try:
                    url = "https://pollinations.ai"
                    files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    data = {
                        "system": "أنت نظام OCR متطور جداً. اقرأ الصورة المرفقة فوراً، واستخرج كل النصوص والكلمات المكتوبة بداخلها بدقة مليمترية تامة وأعد النص المستخرج بنفس لغته الأصلية فقط بدون مقدمات وبدون شروحات.",
                        "private": "true"
                    }
                    
                    response = requests.post(url, data=data, files=files, timeout=25)
                    
                    if response.status_code == 200:
                        extracted_text = response.text.strip()
                        
                        if extracted_text and "sorry" not in extracted_text.lower():
                            st.subheader("🔍 النص المكتشف داخل الصورة حرفياً:")
                            st.code(extracted_text)
                            
                            # الترجمة الاحترافية للنص المستخرج بالمحرك الفولاذي
                            translated_img = fetch_translation(extracted_text, target_lang_text)
                            if translated_img:
                                st.success("✨ **الترجمة الاحترافية المعتمدة لمحتوى الصورة:**")
                                st.info(translated_img)
                            else:
                                st.error("⚠️ تعذر ترجمة النص المستخرج حالياً، يرجى المحاولة مجدداً.")
                        else:
                            st.warning("⚠️ لم يتم العثور على أي نصوص مقروءة أو واضحة داخل هذه الصورة.")
                    else:
                        st.error(f"⚠️ واجه خادم الرؤية البصرية مشكلة، رمز الاستجابة: {response.status_code}")
                except Exception as e:
                    st.error(f"⚠️ عذراً، واجهت مشكلة أثناء فحص واستخراج نصوص الصورة: {str(e)}")
