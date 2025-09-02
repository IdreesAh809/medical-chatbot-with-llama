# 🩺 MEDICAL-LLAMA-CHATBOT

This project is a **medical chatbot** built with **Ollama + Streamlit + FAISS**, designed to provide question–answering based on the open-source book *“Where There Is No Doctor”*.  

🔹 At first, the chatbot used **LLaMA-3:8B**, but since it was too large and slow on CPU, we switched to a **quantized model (`nous-hermes:7b-llama2-q4_K_M`)** for faster inference while still keeping good quality.  
🔹 Everything runs **locally** — no paid GPU or API required.  

---

## 📂 Project Structure

The file structure of the **MEDICAL-LLAMA-CHATBOT** project is as follows:

# medical-chatbot-with-llama
```medical-llama-chatbot/
├── configs/
│   └── config.yml
├── notebooks/
│   └── exploration.ipynb
├── src/
│   ├── data_loader/
│   │   └── pdf_loader.py
│   ├── embeddings/
│   │   └── vector_store.py
│   ├── models/
│   │   └── llama_wrapper.py
│   ├── qa/
│   │   ├── pipeline.py
│   │   └── retriever.py
│   ├── utils/
│   │   └── logger.py
│   └── main.py
├── requirements.txt
└── README.md
```
