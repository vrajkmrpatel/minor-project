import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure the key is loaded
if OPENAI_API_KEY is None:
    raise ValueError("OpenAI API Key not found. Please set it in the .env file.")

print("OpenAI API Key loaded successfully!")
