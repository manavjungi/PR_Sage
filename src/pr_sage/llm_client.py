import google.generativeai as genai

MODEL_NAME = "gemini-flash-latest"

def configure(api_key: str):
    genai.configure(api_key=api_key)

def generate_review(prompt: str) -> str:
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return response.text
