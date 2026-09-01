import streamlit as st
import requests

api_url = "http://127.0.0.1:8000/chat"

st.set_page_config(
    page_title="Medical Agent Chatbot",
    page_icon = "🩺"
)

st.title("Medical Agent Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages=[]


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("How can i help you ?")

if question:
    st.chat_message("user").write(question)
    st.session_state.messages.append(
        {"role": "user",
        "content": question
        }
    )
    
    response = requests.post(
        url=api_url,
        json={"message": question})
    
    if response.status_code == 200:
        data = response.json()
        ans = data["response"]
    else: 
        ans = "Something went wrong , Try again"

    st.chat_message("assistant").write(ans)
    st.session_state.messages.append(
        {"role": "assistant",
         "content": ans
        }
    )
    
    
    
        