import re

import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 20


if "token" not in st.session_state:
    st.session_state.token = None
if "role" not in st.session_state:
    st.session_state.role = None
if "messages" not in st.session_state:
    st.session_state.messages = []


st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.chat-container {
    max-width: 800px;
    margin: auto;
}
.user-msg {
    background-color: #1f2937;
    padding: 12px;
    border-radius: 10px;
    margin: 10px 0;
    text-align: left;
}
.bot-msg {
    background-color: #111827;
    padding: 12px;
    border-radius: 10px;
    margin: 10px 0;
    text-align: left;
    white-space: pre-wrap;
}
</style>
""", unsafe_allow_html=True)


def format_answer(text):
    text = text.strip()
    text = re.sub(r"(?<!\n)(-\s)", r"\n\1", text)
    text = re.sub(r"(?<!\n)(\d+\.\s)", r"\n\1", text)
    return text.strip()


def login(username, password):
    try:
        response = requests.post(
            f"{API_URL}/login",
            params={"username": username, "password": password},
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        return {"error": f"Login request failed: {exc}"}


def chat(query):
    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    try:
        response = requests.get(
            f"{API_URL}/chat",
            params={"query": query},
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        return {"answer": f"❌ Request failed: {exc}"}


st.title("Ask Chatbot!")


if not st.session_state.token:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        result = login(username, password)

        if "access_token" in result:
            st.session_state.token = result["access_token"]
            st.session_state.role = result.get("role", username)
            st.success("Login successful")
            st.rerun()
        else:
            st.error(result.get("error", "Invalid credentials"))

else:
    st.write(f"Logged in as: **{st.session_state.role}**")

    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.role = None
        st.session_state.messages = []
        st.rerun()

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="user-msg">🙍‍♂️ : {msg["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="bot-msg">🤖 : {msg["content"]}</div>',
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

    query = st.chat_input("Type your message...")

    if query:
        st.session_state.messages.append({
            "role": "user",
            "content": query
        })

        result = chat(query)
        answer = format_answer(result.get("answer", "❌ Error fetching response"))

        st.session_state.messages.append({
            "role": "bot",
            "content": answer
        })

        st.rerun()
