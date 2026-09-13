import streamlit as st
import requests

# إعدادات المظهر البرمجي التفاعلي لمنصة صلاح
st.set_page_config(page_title="صانع الأكواد الفوري الذكي", page_icon="💻", layout="centered")

# واجهة الموقع والعناوين الاحترافية
st.title("💻 صانع الأكواد الفوري الذكي")
st.write("حول أفكارك البرمجية إلى أكواد برمجية نظيفة وعالية الجودة في ثوانٍ 🚀")

# صندوق نصي كبير ليكتب فيه المستخدم فكرته البرمجية
user_idea = st.text_area(
    "💡 اكتب فكرتك البرمجية أو المشكلة التي تريد حلها بأي لغة واضحة :", 
    placeholder="مثال: اكتب كود بايثون لإنشاء كلمة مرور عشوائية وقوية...",
    key="input_idea"
)

# زر التوليد التفاعلي
if st.button("🤖 اصنع الكود البرمجي الآن"):
    if user_idea.strip():
        with st.spinner("جاري تحليل الفكرة وهندسة الكود البرمجي..."):
            try:
                # 🛠️ تصحيح تاريخي نهائي: استخدام البوابة النصية النقية المفتوحة التي تقبل التشفير المباشر دون أخطاء الروابط
                base_url = "https://pollinations.ai"
                
                # صياغة الطلب بالإنجليزية في الخلفية لتسريع استجابة الخادم وضمان جودة الكود ومنع خطأ idna تماماً
                prompt_query = (
                    f"Write a complete, functional, high-quality Python script based on this user request: {user_idea}. "
                    f"Output ONLY the raw programming code inside a markdown block. No introductions, no explanations, no HTML code of the website."
                )
                
                headers = {
                    "User-Agent": "Mozilla/5.0"
                }
                
                # بناء الرابط المباشر والمشفر بشكل نقي مخصص للموديل البرمجي qwen-coder
                target_url = f"{base_url}{requests.utils.quote(prompt_query)}?model=qwen-coder&private=true"
                
                response = requests.get(target_url, headers=headers, timeout=25)
                
                if response.status_code == 200:
                    generated_code = response.text.strip()
                    
                    # التحقق من أن النتيجة هي كود برمجي وليست صفحة الموقع
                    if generated_code and "doctype html" not in generated_code.lower() and len(generated_code) > 5:
                        st.success("✨ **تم توليد الكود البرمجي بنجاح وبأعلى جودة :**")
                        # عرض الكود داخل صندوق الماركداون البرمجي الأنيق لسهولة النسخ بلمسة واحدة
                        st.markdown(generated_code)
                    else:
                        st.warning("⚠️ استجاب محرك البرمجة ولكن النتيجة جاءت مبهمة، أعد الضغط على الزر مجدداً لتحديث التوليد واكتب طلبك بوضوح.")
                else:
                    st.error(f"⚠️ واجه خادم البرمجة مشكلة أثناء معالجة الطلب، رمز الاستجابة: {response.status_code}")
                    
            except Exception as e:
                st.error(f"⚠️ عذراً، حدث خطأ أثناء الاتصال بمحرك صناعة الأكواد: {str(e)}")
    else:
        st.warning("⚠️ من فضلك، اكتب فكرتك البرمجية أولاً قبل الضغط على زر التوليد.")
