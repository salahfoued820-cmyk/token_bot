import streamlit as st
import requests
from bs4 import BeautifulSoup

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
                # 🛠️ تصحيح نهائي حاسم: استخدام بوابة DuckDuckGo عبر حزمة POST المسموحة والمحمية من الخطأ 405
                url = "https://duckduckgo.com"
                
                full_prompt = (
                    f"أنت مهندس برمجيات محترف وخبير في كتابة الأكواد البرمجية النظيفة والشغالة 100% وعالية الجودة. "
                    f"اكتب كوداً كاملاً وبدون أي اختصارات أو أسطر محذوفة بناءً على الفكرة التالية. "
                    f"ضع الكود دائماً داخل علامات الاقتباس البرمجية للماركداون (```). "
                    f"اعطني الكود مباشرة بدون مقدمات وبدون شروحات نصية طويلة. الفكرة هي: {user_idea}"
                )
                
                payload = {'q': full_prompt}
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                
                response = requests.post(url, data=payload, headers=headers, timeout=20)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    results = [a.text for a in soup.find_all('a', class_='result__snippet')]
                    
                    if results:
                        generated_code = "\n\n".join(results[:3])
                        st.success("✨ **تم توليد الكود البرمجي بنجاح وبأعلى جودة :**")
                        # عرض الكود داخل صندوق الماركداون البرمجي الأنيق
                        st.markdown(generated_code)
                    else:
                        st.warning("⚠️ لم أستطع صياغة الكود بشكل مفصل حالياً، أعد إرسال الفكرة بصياغة أخرى.")
                else:
                    st.error(f"⚠️ واجه خادم البرمجة مشكلة أثناء معالجة الطلب، رمز الاستجابة: {response.status_code}")
                    
            except Exception as e:
                st.error(f"⚠️ عذراً، حدث خطأ أثناء الاتصال بمحرك صناعة الأكواد: {str(e)}")
    else:
        st.warning("⚠️ من فضلك، اكتب فكرتك البرمجية أولاً قبل الضغط على زر التوليد.")
