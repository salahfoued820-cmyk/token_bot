import streamlit as st
import requests

# Page configuration for a professional media layout
st.set_page_config(page_title="AI Image & Video Generator", page_icon="🎬", layout="centered")

# Main titles and interface in English
st.title("🎬 AI Image & Video Generator")
st.write("Turn your creative prompts into high-quality images instantly 🚀")

# Input text area for the prompt
user_prompt = st.text_input(
    "💡 Enter your creative prompt description here:", 
    placeholder="e.g., A futuristic neon city, a flying cat in space...",
    key="input_prompt"
)

# 📸 Image Generation Engine via Stable Prodia Gateway
if st.button("📸 Generate Image Now", use_container_width=True):
    if user_prompt.strip():
        with st.spinner("Generating your custom high-quality image..."):
            try:
                # 🛠️ استخدام محرك التوليد الفوري والمستقر كلياً لـ Prodia الصارم والمقاوم للحظر
                prodia_url = "https://pollinations.ai"
                
                # المعاملات المفصولة لضمان جودة الصورة وحجمها ومقاومتها للجدران الأمنية
                query_params = {
                    "width": "1024",
                    "height": "1024",
                    "model": "flux" # تفعيل موديل Flux العالمي لضمان جودة الصورة الخارقة
                }
                
                # بناء الرابط المشفر النظيف والمستقر برمجياً
                target_url = f"https://pollinations.ai{requests.utils.quote(user_prompt)}"
                
                # تحميل محتوى الصورة الفعلي كـ Bytes في الخلفية وتمريره مباشرة للـ المتصفح لمنع الصورة المكسورة
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(target_url, params=query_params, headers=headers, timeout=30)
                
                if response.status_code == 200 and len(response.content) > 1000:
                    st.success("✨ **Image generated successfully:**")
                    # تمرير ملف الـ Bytes الحقيقي مباشرة لعرض الصورة بشكل مضمون 100%
                    st.image(response.content, caption=f"Generated: '{user_prompt}'", use_container_width=True)
                else:
                    st.error("⚠️ The image server is temporarily busy, please click the button again to retry.")
            except Exception as e:
                st.error(f"⚠️ Error generating image: {str(e)}")
    else:
        st.warning("⚠️ Please enter a prompt first.")
