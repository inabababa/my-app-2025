import os
from dotenv import load_dotenv
import google.generativeai as genai

def setup_api():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY が環境変数に設定されていません")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("models/gemini-2.5-flash")
