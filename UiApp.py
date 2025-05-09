from openai import OpenAI
import streamlit as st
from Chatbot import Ask
from PIL import Image
import io
from Modules.Database import ImgSerch

# def Description(image):
#     """
#     Analyzes the uploaded image and returns a description.
#     Uses OpenAI's GPT-4 Vision API to generate image descriptions.
#     """
#     try:
#         # Convert image to bytes
#         if isinstance(image, Image.Image):
#             buf = io.BytesIO()
#             image.save(buf, format='PNG')
#             byte_im = buf.getvalue()
#         else:
#             byte_im = image.getvalue()

#         # Create message with image for GPT-4 Vision
#         response = client.chat.completions.create(
#             model="gpt-4-vision-preview",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": "Describe this image in detail"},
#                         {
#                             "type": "image_url",
#                             "image_url": {
#                                 "url": f"data:image/jpeg;base64,{base64.b64encode(byte_im).decode()}"
#                             }
#                         }
#                     ]
#                 }
#             ],
#             max_tokens=300
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         return f"Error analyzing image: {str(e)}"

import os
from dotenv import load_dotenv

load_dotenv()

st.title("🎈MedBot")
st.write("Ask What you want")

# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY not found in environment variables. Please set it in your .env file.")
    st.stop()
client = OpenAI(api_key=OPENAI_API_KEY)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Create two columns for the upload button and chat input
col1, col2 = st.columns([1, 4])

# Add image uploader in the first column
with col1:
    uploaded_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
    
# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Display both text and images if present
        if isinstance(message["content"], dict):
            if "image" in message["content"]:
                st.image(message["content"]["image"])
            st.markdown(message["content"]["text"])
        else:
            st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("What is up?"):
    # Initialize the full prompt
    full_prompt = prompt
    
    # If there's an uploaded image, get its description and add to prompt
    if uploaded_file:
        image_description = ImgSerch(uploaded_file)
        full_prompt = f"Image Description: {image_description}\nUser Question: {prompt}"
        
        # Add user message with both image and text to chat history
        st.session_state.messages.append({
            "role": "user", 
            "content": {
                "text": prompt,
                "image": uploaded_file
            }
        })
    else:
        # Add just the text message to chat history
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

    # Display user message
    with st.chat_message("user"):
        if uploaded_file:
            st.image(uploaded_file)
        st.markdown(prompt)

    # Generate and display AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        stream = Ask(full_prompt)
        
        # Handle the response
        if isinstance(stream, str):
            full_response = stream
        else:
            full_response = ""
            for chunk in stream:
                if hasattr(chunk, 'choices') and chunk.choices:
                    content = chunk.choices[0].delta.get("content", "")
                    full_response += content
                    message_placeholder.markdown(full_response + "▌")
        
        # Display final response
        message_placeholder.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })