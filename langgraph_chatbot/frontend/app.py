import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_URL = os.getenv("API_URL")


st.set_page_config(page_title="LangGraph Chatbot with Wikipedia and Axriv Tools", page_icon="🤖")

if "session_id" not in st.session_state:
    st.session_state.session_id = "user1"  

st.title("🤖 LangGraph Chatbot")

# Chat UI
if "messages" not in st.session_state:
    st.session_state.messages = []

for role, content in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(content)

if prompt := st.chat_input("Type your message..."):
    # User message
    st.session_state.messages.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # API request
    response = requests.post(API_URL, json={"session_id": st.session_state.session_id, "message": prompt})
    bot_reply = response.json()["response"]

    # Assistant message
    st.session_state.messages.append(("assistant", bot_reply))
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
