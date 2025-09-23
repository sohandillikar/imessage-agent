import os
import utils
from datetime import datetime

# https://platform.openai.com/docs/guides/function-calling
# If your function has no return value (e.g. send_email),
# simply return a string to indicate success or failure. (e.g. "success")

file_path = f"./{os.path.basename(__file__)}"
tools = utils.get_tools_list(file_path, avoid_functions=["call_function"], web_search=True)

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

# TODO: Add f-strings for the user's name
def get_user_info() -> dict:
    """
    Get information about Sohan Dillikar.
    Returns:
        dict: Sohan Dillikar's email, phone, nicknames, occupation, relation, background, interests
    """
    return utils.get_user_info()

def call_function(name: str, args: dict):
    if name == "get_current_date":
        return get_current_date(**args)
    elif name == "get_current_time":
        return get_current_time(**args)
    elif name == "get_user_info":
        return get_user_info(**args)
    else:
        raise ValueError(f"Function {name} not found")