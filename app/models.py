from langchain_groq import ChatGroq
from .config import GROQ_API_KEY, GROQ_MODEL

def get_llm():
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is missing. Add it to your .env file.")
    return ChatGroq(
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0.3,
    )
