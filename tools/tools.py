import glob
from datetime import datetime
from tools.utils import get_tools_list
import knowledgebase.people.tools as people_tools

# https://platform.openai.com/docs/guides/function-calling
# If your function has no return value (e.g. send_email),
# simply return a string to indicate success or failure. (e.g. "success")

# Create tools list
tools_list = get_tools_list(__file__, avoid_functions=["call_function"], web_search=True)
tools_files = glob.glob("knowledgebase/**/tools.py", recursive=True)
for file in tools_files:
    tools_list += get_tools_list(file)

def get_current_date() -> str:
    """
    Get the current date.
    Returns:
        str: The current date formatted as "Friday September 20, 2025"
    """
    return datetime.now().strftime("%A %B %d, %Y")

def get_current_time() -> str:
    """
    Get the current time.
    Returns:
        str: The current time formatted as "10:00 AM"
    """
    return datetime.now().strftime("%I:%M %p")

def call_function(name: str, args: dict):
    if name == "get_current_date":
        return get_current_date(**args)
    elif name == "get_current_time":
        return get_current_time(**args)
    elif name == "get_user_email":
        return people_tools.get_user_email(**args)
    elif name == "get_user_phone":
        return people_tools.get_user_phone(**args)
    elif name == "get_user_interests":
        return people_tools.get_user_interests(**args)
    else:
        raise ValueError(f"Function '{name}' not found")