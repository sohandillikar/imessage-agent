import os
import openai_utils
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def setup() -> OpenAI:
    if os.getenv("OPENAI_API_KEY") is None:
        raise ValueError("OPENAI_API_KEY is not set in .env")
    if os.getenv("COUNTRY") is None:
        raise ValueError("COUNTRY is not set in .env")
    if os.getenv("TIMEZONE") is None:
        raise ValueError("TIMEZONE is not set in .env")
    
    # Check if knowledge_base vector store exists
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    openai_utils.get_knowledge_base(client)
    
    return client

if __name__ == "__main__":
    setup()