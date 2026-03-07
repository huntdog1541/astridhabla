import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import os

# This loads the variables from the .env file
load_dotenv()

# Now os.getenv will find them
PASSWORD = os.getenv("MY_CHAT_PASSWORD")
API_KEY = os.getenv("DEEPINFRA_TOKEN")

# 1. Configuration
# PASSWORD = os.environ.get("MY_CHAT_PASSWORD", "test123")
# Use DeepInfra or your local Ollama address
# API_KEY = os.environ.get("DEEPINFRA_TOKEN", "your_token")
BASE_URL = "https://api.deepinfra.com/v1/openai"

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if not st.session_state["authenticated"]:
        user_pass = st.text_input("Contraseña", type="password")
        if st.button("Entrar"):
            if user_pass == PASSWORD:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
        return False
    return True

if check_password():
    st.title("Mi Asistente IA")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    # 2. Set the System Prompt to force Spanish
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": "Eres un asistente inteligente. SIEMPRE debes responder en español, de forma clara y concisa."
            }
        ]

    # Display chat (Hide the system message from the user)
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("¿En qué puedo ayudarte?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="meta-llama/Meta-Llama-3-8B-Instruct", # Or your preferred model
                messages=st.session_state.messages,
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
