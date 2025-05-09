from openai import OpenAI
import streamlit as st
from Chatbot import Ask
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()

tab1, tab2 = st.tabs(["Text", "Audio"])

with tab1:
    st.title("☤ MedBot")
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

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # Handle new user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display AI response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            stream = Ask(prompt)
            
            # If stream is already a string, use it directly
            if isinstance(stream, str):
                full_response = stream
            else:
                # If it's a stream, accumulate the response
                full_response = ""
                for chunk in stream:
                    if hasattr(chunk, 'choices') and chunk.choices:
                        content = chunk.choices[0].delta.get("content", "")
                        full_response += content
                        message_placeholder.markdown(full_response + "▌")
            
            # Display final response
            message_placeholder.markdown(full_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

