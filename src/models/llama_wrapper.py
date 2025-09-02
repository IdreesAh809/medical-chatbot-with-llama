import ollama

#1st try the llama3:8b model but the response time is too much slow on cpu. then try the nous-hermes:7b-llama2-q4_K_M model which is quantized and faster
class OllamaWrapper:
    def __init__(self, model_name="nous-hermes:7b-llama2-q4_K_M", temperature=0.2, timeout=30, max_tokens=150):
        self.model_name = model_name
        self.temperature = temperature
        self.timeout = timeout
        self.max_tokens = max_tokens
        self.chat_history = []

    def generate(self, prompt: str) -> str:
        """Single-turn response (no memory)."""
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                options={
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens  # 🔑 limit output
                },
            )
            return response["message"]["content"].strip()
        except Exception as e:
            return f"Error running model: {e}"

    def chat(self, user_input: str) -> str:
        """Multi-turn chat with history."""
        self.chat_history.append({"role": "user", "content": user_input})

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=self.chat_history,
                options={
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens  # 🔑 apply here too
                },
            )
            reply = response["message"]["content"].strip()
            self.chat_history.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            return f"Error running model: {e}"

    def reset(self):
        """Clear the chat history."""
        self.chat_history = []