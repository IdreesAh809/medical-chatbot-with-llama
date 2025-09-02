# src/main.py
import sys, os
import streamlit as st

# Ensure src folder is in Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from embeddings.vector_store import load_index, query_index
from qa.pipeline import answer_question
from utils.logger import setup_logger
from models.llama_wrapper import OllamaWrapper

# Initialize logger
logger = setup_logger(name="chatbot_logger", log_file="logs/app.log")

# Initialize model wrapper in session
if "llm" not in st.session_state:
    st.session_state.llm = OllamaWrapper(
        # Old model (slower, accurate):
        # model_name="llama3:8b"
        # New model (faster, quantized):
        model_name="nous-hermes:7b-llama2-q4_K_M"
    )

# Load FAISS index on app start
try:
    load_index()
    logger.info("✅ FAISS index loaded successfully!")
except Exception as e:
    logger.error(f"⚠️ Index not loaded: {e}")
    st.warning(f"⚠️ Index not loaded: {e}")

st.title("🩺 Health Assistant  –  No Clinic")



# Reset button
if st.button("🔄 Reset Conversation"):
    st.session_state.llm.reset()
    st.success("Conversation history cleared!")
    logger.info("Conversation reset.")

# Display past messages
for msg in st.session_state.llm.chat_history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# Input box
if user_input := st.chat_input("Ask a medical question:"):
    logger.info(f"User asked: {user_input}")

    # Show user message
    st.chat_message("user").write(user_input)

    with st.spinner("Fetching answer..."):
        # Retrieve relevant chunks (still used to keep answers grounded)
        chunks = query_index(user_input, top_k=3)
        logger.info(f"Retrieved {len(chunks)} chunks for query.")

        # Get model response (multi-turn)
        response = st.session_state.llm.chat(user_input)
        logger.info(f"Model response: {response[:200]}...")

    # Show assistant message
    st.chat_message("assistant").write(response)
