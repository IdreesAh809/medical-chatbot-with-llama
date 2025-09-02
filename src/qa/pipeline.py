# src/qa/pipeline.py
def answer_question(user_question: str, concise=True) -> str:
    try:
        context_chunks = query_index(user_question, top_k=3)
        context_text = "\n".join(context_chunks)

        concise_instruction = "Answer briefly in 3–4 bullet points." if concise else ""

        prompt = f"""
        You are a helpful medical assistant.
        Context: {context_text}
        Question: {user_question}
        {concise_instruction}
        Answer:
        """

        return llm.generate(prompt)
    except Exception as e:
        return f"Error in pipeline: {e}"
