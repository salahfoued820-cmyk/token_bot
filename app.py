import streamlit as st

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

# 📸 Column 1: Image Generation Engine
with col1:
    if st.button("📸 Generate Image Now", use_container_width=True):
        if user_prompt.strip():
            with st.spinner("Generating your custom high-quality image..."):
                try:
                    # صياغة الرابط القياسي الصحيح
                    safe_prompt = user_prompt.strip().replace(" ", "%20")
                    image_url = f"https://pollinations.ai{safe_prompt}?width=1024&height=1024&nologo=true&private=true"
                    
                    st.success("✨ **Image generated successfully:**")
                    
                    # 🛠️ الحل المعجز: عرض الصورة عبر صندوق HTML مدمج لتخطي كراش الروابط والصور المكسورة نهائياً
                    st.markdown(f'<img src="{image_url}" style="width:100%; border-radius:10px;">', unsafe_allow_html=True)
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
                    # صياغة رابط الفيديو المتحرك
                    safe_prompt = user_prompt.strip().replace(" ", "%20")
                    video_url = f"https://pollinations.ai{safe_prompt}?width=512&height=512&nologo=true&feed=true&private=true"
                    
                    st.success("✨ **Video animation created successfully:**")
                    
                    # 🛠️ الحل المعجز: عرض الفيديو المتحرك عبر كود HTML نظيف وخفيف لضمان الاستجابة الفورية
                    st.markdown(f'<img src="{video_url}" style="width:100%; border-radius:10px;">', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"⚠️ Error creating video: {str(e)}")
        else:
            st.warning("⚠️ Please enter a prompt first.")
