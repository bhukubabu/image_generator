import streamlit as st
from matplotlib import pyplot as plt
import requests
import io
from PIL import Image
import time

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
api_token ='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'
headers = {"Authorization": f"Bearer {api_token}"}

st.title("AI Art🎨 Generator ✨")
st.subheader('',divider='rainbow')
st.subheader("Hello I am your AI art 👨‍🎨assistant. I will generate artworks for you😊 Let's try ............")

with st.container(height= 180):
    prompt = st.text_area('Type your prompt here')

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content



but1 = st.button("Generate")

if but1:
    if prompt == "":
        st.error('Please provide a valid prompt', icon="🚨")
    else:
        with st.spinner("Please wait......."):
            image_bytes = query({
                "inputs": prompt,
                "parameters": {
                    "guidance_scale": 8.6,
                    "num_inference_steps": 90,
                }
            })

            images = Image.open(io.BytesIO(image_bytes))
        st.success('Done!')
        # Display image directly without saving
        st.image(images)
        with io.BytesIO() as img_buffer:
            images.save(img_buffer, format="JPEG")
            img_buffer.seek(0)
            but2 = st.download_button(
                label="Download",
                data=img_buffer,
                file_name='images.jpg',
                mime='image/jpg'
            )
