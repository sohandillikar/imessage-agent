import glob
from datetime import datetime
from tools.utils import get_tools_list
import knowledgebase.people.tools as people_tools

# https://platform.openai.com/docs/guides/function-calling
# If your function has no return value (e.g. send_email),
# simply return a string to indicate success or failure. (e.g. "success")

# Create tools list
tools_list = get_tools_list(__file__, avoid_functions=["call_function"], web_search=True, file_search=True)
"""
tools_files = glob.glob("knowledgebase/**/tools.py", recursive=True)
for file_path in tools_files:
    folder_name = file_path.split("/")[-2]
    tools_list += get_tools_list(file_path, module_name=folder_name, avoid_functions=["call_function"])
"""

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
    if name == "get_current_time":
        return get_current_time(**args)
    if name.startswith("people-"):
        return people_tools.call_function(name.split("-")[1], args)
    raise ValueError(f"Function '{name}' not found")