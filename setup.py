import os
import openai_utils
from dotenv import load_dotenv
from openai import OpenAI
from tools.journals.utils import load_journals

load_dotenv()

# Give full disk access to Terminal or IDE
# Give location permissions to Python

def setup(update_knowledge_base: bool = True) -> OpenAI:
    env_vars = ["IMESSAGES_DB_PATH", "CONTACTS_DB_PATH", "OPENAI_API_KEY", "COUNTRY", "TIMEZONE"]
    for env_var in env_vars:
        if not os.getenv(env_var):
            raise ValueError(f"{env_var} is not set in .env")
    
    # Check if knowledge_base vector store exists
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    knowledge_base = openai_utils.get_knowledge_base(client)
    if update_knowledge_base:
        load_journals(new_only=False)
        openai_utils.update_knowledge_base(client, knowledge_base)
    
    return client

if __name__ == "__main__":
    setup()