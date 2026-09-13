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
                    clean_prompt = requests.utils.quote(user_prompt)
                    image_url = f"https://pollinations.ai{clean_prompt}?width=1024&height=1024&nologo=true&private=true"
                    
                    # Téléchargement des octets réels de l'image pour éviter l'affichage brisé
                    response = requests.get(image_url, headers=headers, timeout=20)
                    
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
                    clean_prompt = requests.utils.quote(user_prompt)
                    video_url = f"https://pollinations.ai{clean_prompt}?width=512&height=512&nologo=true&feed=true&private=true"
                    
                    # Téléchargement des octets réels de l'animation pour éviter l'affichage brisé
                    response = requests.get(video_url, headers=headers, timeout=25)
                    
                    if response.status_code == 200:
                        st.success("✨ **Video animation created successfully:**")
                        st.image(response.content, caption=f"Animation: '{user_prompt}'", use_container_width=True)
                    else:
                        st.error(f"⚠️ Video server responded with status code: {response.status_code}")
                except Exception as e:
                    st.error(f"⚠️ Error creating video: {str(e)}")
        else:
            st.warning("⚠️ Please enter a prompt first.")
