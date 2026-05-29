import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY")