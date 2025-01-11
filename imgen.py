import streamlit as st
import requests
import io
from PIL import Image
import time


if "prompt" not in st.session_state:
    st.session_state.prompt = ""


def fetch_prompt(prompt):
    st.session_state.prompt = prompt


def gen_from_query(payload):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    api_token = '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'
    headers = {"Authorization": f"Bearer {api_token}"}
    retries=4 #this will change as per the hugging face token limit
    
    for i in range(retries):
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.content  
        else:
            #st.error(f"Error: {response.status_code} - {response.text}")
            st.warning(f"failed to fetch response for {i+1}, retrying.....")
            time.sleep(2)


#----------------------- main interface -----------------------#

st.title("AI Art🎨 Generator ✨")
st.subheader('', divider='rainbow')
st.subheader("Hello I am your AI art 👨‍🎨assistant. I will generate artworks for you😊 Let's try ............")
with st.container(height=280):
    prompt = st.text_area('Type your prompt here', height=160)
but1 = st.button("Generate", on_click=fetch_prompt, args=(prompt,))

if but1:
    if prompt == "":
        st.error('Please provide a valid prompt', icon="🚨")
    else:
        with st.spinner("Please wait......."):
            image_bytes = gen_from_query({
                "inputs": st.session_state.prompt,
                "parameters": {
                    "guidance_scale": 8.6,
                    "num_inference_steps": 90,
                }
            })
        
        if image_bytes:
            try:
                images = Image.open(io.BytesIO(image_bytes))
            except Exception as e:
                st.error(f"Error opening the image: {str(e)}")
                st.rerun()
            st.success('Done!')
            st.image(images)  
            with io.BytesIO() as img_buffer:
                    images.save(img_buffer, format="JPEG")
                    img_buffer.seek(0)
                    st.download_button(
                        label="Download",
                        data=img_buffer,
                        file_name='images.jpg',
                        mime='image/jpg'
                    )
              # Clear the cache if there's an issue
        else:
            st.error("Failed to generate an image. Please try again.")
