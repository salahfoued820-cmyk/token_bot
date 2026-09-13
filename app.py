import streamlit as st
import requests

# Page configuration for a professional media layout
st.set_page_config(page_title="AI Image & Video Generator", page_icon="🎬", layout="centered")

# Main titles and interface in English
st.title("🎬 AI Image & Video Generator")
st.write("Turn your creative prompts into high-quality images and animated videos instantly 🚀")

# Input text area for the prompt
user_prompt = st.text_input(
    "💡 Enter your creative prompt description here:", 
    placeholder="e.g., A futuristic neon city, a flying cat in space...",
    key="input_prompt"
)

# Creating two columns for the buttons
col1, col2 = st.columns(2)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# 📸 Column 1: Image Generation Engine
with col1:
    if st.button("📸 Generate Image Now", use_container_width=True):
        if user_prompt.strip():
            with st.spinner("Generating your custom high-quality image..."):
                try:
                    # 🛠️ تصحيح تاريخي: ترك الرابط الرئيسي نقياً وقصيراً جداً لمنع خطأ الالتصاق والـ NameResolutionError
                    base_url = "https://pollinations.ai"
                    
                    # تمرير النص وباقي الإعدادات كمعاملات منفصلة برمجياً لضمان سلامة الرابط 100%
                    query_params = {
                        "width": "1024",
                        "height": "1024",
                        "nologo": "true",
                        "private": "true"
                    }
                    
                    # بناء الرابط المشفر النظيف بشكل حركي آمن
                    target_url = f"{base_url}{requests.utils.quote(user_prompt)}"
                    
                    # تنزيل الملف الفعلي لضمان العرض المباشر وبدون أي حظر
                    response = requests.get(target_url, params=query_params, headers=headers, timeout=25)
                    
                    if response.status_code == 200:
                        st.success("✨ **Image generated successfully:**")
                        st.image(response.content, caption=f"Generated: '{user_prompt}'", use_container_width=True)
                    else:
                        st.error(f"⚠️ Image server responded with status code: {response.status_code}")
                except Exception as e:
                    st.error(f"⚠️ Error generating image: {str(e)}")
        else:
            st.warning("⚠️ Please enter a prompt first.")

# 🎥 Column 2: Video/Animation Generation Engine
with col2:
    if st.button("🎥 Create Video Animation", use_container_width=True):
        if user_prompt.strip():
            with st.spinner("Creating your custom video animation loop..."):
                try:
                    # 🛠️ تصحيح تاريخي: فصل الرابط عن المتغيرات لمنع التشويه
                    base_url = "https://pollinations.ai"
                    
                    query_params = {
                        "width": "512",
                        "height": "512",
                        "nologo": "true",
                        "feed": "true",
                        "private": "true"
                    }
                    
                    target_url = f"{base_url}{requests.utils.quote(user_prompt)}"
                    
                    response = requests.get(target_url, params=query_params, headers=headers, timeout=25)
                    
                    if response.status_code == 200:
                        st.success("✨ **Video animation created successfully:**")
                        st.image(response.content, caption=f"Animation: '{user_prompt}'", use_column_width=True)
                    else:
                        st.error(f"⚠️ Video server responded with status code: {response.status_code}")
                except Exception as e:
                    st.error(f"⚠️ Error creating video: {str(e)}")
        else:
            st.warning("⚠️ Please enter a prompt first.")
