import os

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# load env values
load_dotenv()

llm = ChatGroq(model=os.environ.get("GROQ_LLM_MODEL"), temperature=0.0)
system_role = {"role": "system", "content": "You are a helpful assistant"}

def get_user_name() -> str:
    user_name = st.session_state.get("user_name")
    if not user_name:
        for x in range(10):
            user_name = input("Enter your user name: ")
            if user_name:
                st.session_state.user_name = user_name.title()
                break

    st.session_state.user_name = user_name.title()
    return user_name.title()



client_name = get_user_name()


# welcome user and request to start the conversation
st.title(f"Hello {client_name}! Let's chat!")

# initialise UI
st.set_page_config(
    page_title="ChatBot",
    page_icon="🗣",
    layout="centered",
    initial_sidebar_state="auto",
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# print("chat history initialized")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)


user_prompt = st.chat_input("your thoughts...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt, unsafe_allow_html=True)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    response = llm.invoke(
        input=[
            system_role,
            {"role": "user", "content": user_prompt},
            *st.session_state.chat_history,
        ]
    )
    assistant_response = response.content
    st.session_state.chat_history.append(
        {"role": "assistant", "content": assistant_response}
    )

    with st.chat_message("assistant"):
        st.markdown(assistant_response, unsafe_allow_html=True)



