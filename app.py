# streamlit_text_to_video.py
# Web interface for Text-to-Video Generator using Streamlit

import streamlit as st
from gtts import gTTS
from moviepy import ImageClip, AudioFileClip
from PIL import Image
import os
st.title("📽️ Text to Video Generator")
st.markdown("Convert any text into a narrated video with one click!")

# Text input
txt_input = st.text_area("Enter your text:", "The solar system has 8 planets. Earth is the third planet from the sun.")

# Upload or use default image
bg_image = st.file_uploader("Upload a background image (optional)", type=["jpg", "png"])

if st.button("Generate Video"):
    with st.spinner("Generating video..."):
        # Save uploaded image or create default one
        image_path = "background.jpg"
        if bg_image is not None:
            with open(image_path, "wb") as f:
                f.write(bg_image.read())
        else:
            img = Image.new('RGB', (1280, 720), color=(30, 144, 255))
            img.save(image_path)

        # Generate audio
        tts = gTTS(text=txt_input, lang='en')
        audio_path = "output_audio.mp3"
        tts.save(audio_path)

        # Create video
        audio_clip = AudioFileClip(audio_path)
        image_clip = ImageClip(image_path).with_duration(audio_clip.duration)
        final_video = image_clip.with_audio(audio_clip).with_duration(audio_clip.duration)

        video_path = "text_to_video.mp4"
        final_video.write_videofile(video_path, fps=24)

        # Show video
        st.success("Video generated successfully!")
        st.video(video_path)

        # Cleanup (optional)
        # os.remove(audio_path)
        # os.remove(image_path)
