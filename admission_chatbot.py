import os
import json
from ai import get_openai_chat_response

with open("./test-data/admission.json", "r", encoding="utf8") as f:
    data = json.load(f)


set_the_tone = "You are Denison University's admission assistant. Only answer questions about Denison University and it's admission process cheerful, short and sweet. Use paragraphs. Keep answers to less than 15 sentences."


def get_admission_chatbot_response(user_reply):
    return get_openai_chat_response(data, user_reply, set_the_tone)
