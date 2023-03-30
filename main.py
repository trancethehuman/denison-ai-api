import streamlit as st

from admission_chatbot import get_admission_chatbot_response

st.title("Denison University AI Tools Demo")

st.subheader("1. Admission AI Assistant")

user_response = st.text_input(
    "Type your question and hit Enter!", max_chars=80)

if (user_response):
    with st.spinner('Wait for it...'):
        st.write(get_admission_chatbot_response(user_response))
