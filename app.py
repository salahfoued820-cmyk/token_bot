import streamlit as st
import requests
from deep_translator import GoogleTranslator

# إعدادات الصفحة البرمجية لـ Streamlit
st.set_page_config(page_title="منصة صلاح للترجمة الذكية", page_icon="🌐", layout="centered")

# واجهة الموقع والعناوين
st.title("🌐 منصة صلاح العالمية للترجمة الذكية")
st.write("ترجمة النصوص والصور فوراً بأحدث التقنيات السحابية مجاناً 🚀")

# قائمة اللغات المتاحة مع أكوادها الرسمية
LANGUAGES = {
    "العربية": "ar",
    "الإنجليزية (English)": "en",
    "الفرنسية (Français)": "fr",
    "الألمانية (Deutsch)": "de",
    "الإيطالية (Italiano)": "it",
    "الإسبانية (Español)": "es"
}

# قائمة منسدلة تفاعلية لاختيار اللغة
target_lang_name = st.selectbox("🎯 اختر اللغة التي تريد الترجمة إليها:", list(LANGUAGES.keys()))
target_lang_code = LANGUAGES[target_lang_name]

# إنشاء تبويبات لفصل نظام النصوص عن الصور
tab1, tab2 = st.tabs(["📝 ترجمة النصوص", "📸 ترجمة الصور"])

with tab1:
    user_text = st.text_area("✏️ اكتب أو الصق النص المراد ترجمته هنا:", placeholder="Hello my friend...", key="input_text")
    if st.button("🔄 ترجم النص الآن", key="btn_text"):
        if user_text.strip():
            with st.spinner("جاري معالجة الترجمة..."):
                try:
                    # استخدام المحرك الحديث والمستقر 100% المتوافق مع بايثون الحديثة
                    translated_text = GoogleTranslator(source='auto', target=target_lang_code).translate(user_text)
                    st.success("✨ **الترجمة الاحترافية المعتمدة:**")
                    st.info(translated_text)
                except Exception as e:
                    st.error(f"⚠️ عذراً، حدث خطأ أثناء الاتصال بمحرك الترجمة: {str(e)}")
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
                            
                            # الترجمة الاحترافية للنص المستخرج بالمحرك الحديث
                            translated_img = GoogleTranslator(source='auto', target=target_lang_code).translate(extracted_text)
                            st.success("✨ **الترجمة الاحترافية المعتمدة لمحتوى الصورة:**")
                            st.info(translated_img.text)
                        else:
                            st.warning("⚠️ لم يتم العثور على أي نصوص مقروءة أو واضحة داخل هذه الصورة.")
                    else:
                        st.error(f"⚠️ واجه خادم الرؤية البصرية مشكلة، رمز الاستجابة: {response.status_code}")
                except Exception as e:
                    st.error(f"⚠️ عذراً، واجهت مشكلة أثناء فحص واستخراج نصوص الصورة: {str(e)}")
