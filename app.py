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
                # 🛠️ تصحيح تاريخي: استخدام البوابة النصية المباشرة والمحسنة عبر GET نظيف بدون معاملات JSON معقدة
                # هذه البوابة مسموحة كلياً وتعيد نصوص الأكواد الصافية فوراً
                base_url = "https://pollinations.ai"
                
                # صياغة واضحة ومباشرة باللغة الإنجليزية في الخلفية لتسريع استجابة الخادم وضمان جودة الكود
                prompt_query = f"Write a complete, functional, high-quality script based on this idea: {user_idea}. Output ONLY the raw programming code inside a markdown block. No introductions, no explanations, no chat."
                
                headers = {
                    "User-Agent": "Mozilla/5.0"
                }
                
                # بناء الرابط المشفر بشكل آمن لحماية السيرفر
                target_url = f"{base_url}{requests.utils.quote(prompt_query)}"
                
                response = requests.get(target_url, headers=headers, timeout=20)
                
                if response.status_code == 200:
                    generated_code = response.text.strip()
                    
                    if generated_code and len(generated_code) > 5 and "sorry" not in generated_code.lower():
                        st.success("✨ **تم توليد الكود البرمجي بنجاح وبأعلى جودة :**")
                        # عرض الكود داخل صندوق الماركداون البرمجي الأنيق لسهولة النسخ
                        st.markdown(generated_code)
                    else:
                        st.warning("⚠️ استجاب محرك البرمجة ولكن النتيجة جاءت مبهمة، أعد الضغط على الزر مجدداً لتحديث التوليد.")
                else:
                    st.error(f"⚠️ واجه خادم البرمجة مشكلة أثناء معالجة الطلب، رمز الاستجابة: {response.status_code}")
                    
            except Exception as e:
                st.error(f"⚠️ عذراً، حدث خطأ أثناء الاتصال بمحرك صناعة الأكواد: {str(e)}")
    else:
        st.warning("⚠️ من فضلك، اكتب فكرتك البرمجية أولاً قبل الضعم على زر التوليد.")
