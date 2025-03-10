import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st

import google.generativeai as genai

api_key = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key = api_key)
model = genai.GenerativeModel("gemini-1.5-pro")
chat = model.start_chat(history=[])


def generate_response(question):
    response = chat.send_message(question,stream=True)
    return response
   


st.set_page_config(page_title="Convernational Q&A Demo")
st.title("Q&A Demo")

with st.sidebar:
    api_key = st.text_input("Please enter your Gemini Api Key" ,type="password")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

input = st.text_input("User Input", key = "input")
submit = st.button("Ask Your Question")

if submit and input:
    response = generate_response(input)
    st.session_state["messages"].append(("User",input))
    st.subheader("The Response is ...")
    for chunk_history in response:
        st.write(chunk_history.text)
        st.session_state["messages"].append(("Bot",chunk_history.text))

st.subheader("The Chat History")

for role, text in st.session_state["messages"]:
    st.write(f"{role}:{text}")


