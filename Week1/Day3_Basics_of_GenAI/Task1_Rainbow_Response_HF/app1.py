import streamlit as st
from groq import Groq

# 🔑 Put your Groq API key here
API_KEY = "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"

# Initialize Groq client
client = Groq(api_key=API_KEY)

st.title("🤖 Ask Groq AI")

# User input box
user_question = st.text_input("Enter your question:", "Explain how rainbows are formed")

if st.button("Ask"):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # Groq model
            messages=[{"role": "user", "content": user_question}]
        )
        answer = response.choices[0].message.content
        st.subheader("Response:")
        st.write(answer)
    except Exception as e:
        st.error(f"Error: {e}")
