import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
