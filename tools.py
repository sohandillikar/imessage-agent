from datetime import datetime
from typing import Any

# https://platform.openai.com/docs/guides/function-calling
# If your function has no return value (e.g. send_email),
# simply return a string to indicate success or failure. (e.g. "success")

def get_current_date() -> str:
    """
    Get the current date.
    Example: Friday September 20, 2025
    """
    return datetime.now().strftime("%A %B %d, %Y")

def get_current_time() -> str:
    """
    Get the current time.
    Example: 10:00 AM
    """
    return datetime.now().strftime("%I:%M %p")

def call_function(name: str, args: dict):
    if name == "get_current_date":
        return get_current_date(**args)
    elif name == "get_current_time":
        return get_current_time(**args)
    else:
        raise ValueError(f"Function {name} not found")

tools = [
    {
        "type": "function",
        "name": "get_current_date",
        "description": "Get the current date.\nExample: Friday September 20, 2025",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "type": "function",
        "name": "get_current_time",
        "description": "Get the current time.\nExample: 10:00 AM",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "type": "web_search",
        "user_location": {
            "type": "approximate",
            "country": "US",
            "timezone": "America/Los_Angeles"
        }
    }
]