import streamlit as st
import requests

st.set_page_config(page_title="💬 LLM Chatbot", layout="wide")

#  Session State 
if "messages" not in st.session_state:
    st.session_state.messages = []

#  Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")

    provider = st.selectbox(
        "Choose Model Provider",
        ["Google Gemini", "OpenRouter", "Groq"]
    )

    if provider == "Google Gemini":
        st.markdown("[🔑 Get Gemini API Key](https://makersuite.google.com/app/apikey)")
        api_key = st.text_input("Enter Gemini API Key", type="password")
        model = st.selectbox("Choose Model", ["gemini-1.5-flash", "gemini-1.5-pro"])

    elif provider == "OpenRouter":
        st.markdown("[🔑 Get OpenRouter API Key](https://openrouter.ai/keys)")
        api_key = st.text_input("Enter OpenRouter API Key", type="password")
        model = st.selectbox("Choose Model", [
            "mistralai/mistral-7b-instruct:free",
            "meta-llama/llama-3-8b-instruct:free",
            "google/gemma-7b-it:free",
            "google/gemini-2.0-flash-exp:free",
            "google/gemma-3-27b-it:free",
            "google/gemma-3-4b-it:free",
            "mistralai/devstral-small:free"
        ])

    elif provider == "Groq":
        st.markdown("[🔑 Get Groq API Key](https://console.groq.com/keys)")
        api_key = st.text_input("Enter Groq API Key", type="password")
        model = st.selectbox("Choose Model", [
            "llama3-8b-8192",
            "llama3-70b-8192"
        ])

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []

# Chat Display
st.title("💬 LLM Chatbot")
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    reply = "⚠️ No response yet."

    if api_key:
        try:
            if provider == "Google Gemini":
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
                headers = {"Content-Type": "application/json"}
                params = {"key": api_key}
                payload = {"contents": [{"parts": [{"text": prompt}]}]}

                response = requests.post(url, headers=headers, params=params, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    reply = data["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    reply = f"Error {response.status_code}: {response.text}"

            elif provider == "OpenRouter":
                url = "https://openrouter.ai/api/v1/chat/completions"
                headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                payload = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}]
                }

                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    reply = data["choices"][0]["message"]["content"]
                else:
                    reply = f"Error {response.status_code}: {response.text}"

            elif provider == "Groq":
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                payload = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}]
                }

                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    reply = data["choices"][0]["message"]["content"]
                else:
                    reply = f"Error {response.status_code}: {response.text}"

        except Exception as e:
            reply = f"⚠️ Exception: {str(e)}"
    else:
        st.warning("Please enter your API key in the sidebar.")

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").markdown(reply)

