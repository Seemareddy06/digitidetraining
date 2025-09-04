import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from google import genai

# 1. Gemini API Setup
API_KEY = "AIzaSyAvQvP_ZHlN40_Y_Rn_zVADZHZ0kKfv5k0"   
client = genai.Client(api_key=API_KEY)

def call_gemini(prompt, model="gemini-2.5-flash"):
    """Send a query to Gemini API and return response"""
    try:
        resp = client.models.generate_content(
            model=model,
            contents=prompt
        )
        return resp.text
    except Exception as e:
        return f"❌ Gemini API Error: {str(e)}"

# 2. Load Data into Vector Store
def load_vectorstore():
    # Example files
    salary_text = """Monthly salary is the amount an employee earns each month.
    Annual salary is monthly salary × 12.
    Deductions include income tax, provident fund, professional tax, and insurance premiums.
    Net salary = Gross salary - Deductions."""

    insurance_text = """Insurance benefits include health coverage, accident protection, and life insurance.
    Premium is the amount paid monthly or annually for coverage.
    Claims are processed by submitting required documents to the insurance provider."""

    docs = [
        Document(page_content=salary_text, metadata={"topic": "salary"}),
        Document(page_content=insurance_text, metadata={"topic": "insurance"}),
    ]

    splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    splits = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(splits, embeddings)
    return vectorstore

# 3. Agent Logic
def salary_agent(query, vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    docs = retriever.get_relevant_documents(query)
    context = "\n".join([d.page_content for d in docs if "salary" in d.metadata["topic"]])
    if not context:
        return "Sorry, I can only answer salary-related queries."
    return call_gemini(f"Context:\n{context}\n\nQuestion: {query}\nAnswer:")

def insurance_agent(query, vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    docs = retriever.get_relevant_documents(query)
    context = "\n".join([d.page_content for d in docs if "insurance" in d.metadata["topic"]])
    if not context:
        return "Sorry, I can only answer insurance-related queries."
    return call_gemini(f"Context:\n{context}\n\nQuestion: {query}\nAnswer:")

def coordinator_agent(query):
    """Gemini decides whether SALARY or INSURANCE agent should handle the query"""
    system_prompt = f"""
    You are a coordinator. Decide who should answer the query.
    Query: "{query}"
    Options: SALARY or INSURANCE
    Reply with only one word: SALARY or INSURANCE
    """
    resp = call_gemini(system_prompt)
    return resp.strip().upper()

# 4. Streamlit App
st.set_page_config(page_title="Multi-Agent RAG System", page_icon="🤖")
st.title("🤖 Multi-Agent RAG System with Gemini")

if "messages" not in st.session_state:
    st.session_state.messages = []

vectorstore = load_vectorstore()

# Chat Interface
user_query = st.chat_input("Ask me about Salary or Insurance...")
if user_query:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Decide which agent to call
    agent_choice = coordinator_agent(user_query)

    if "SALARY" in agent_choice:
        answer = salary_agent(user_query, vectorstore)
    elif "INSURANCE" in agent_choice:
        answer = insurance_agent(user_query, vectorstore)
    else:
        answer = " Sorry, I could not determine the right agent."

    st.session_state.messages.append({"role": "assistant", "content": answer})

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

