from datetime import datetime
import knowledge_base.people.tools as people_tools

# https://platform.openai.com/docs/guides/function-calling
# If your function has no return value (e.g. send_email),
# simply return a string to indicate success or failure. (e.g. "success")

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
    module, func = name.split("-")
    if module == "tools":
        if func == "get_current_date":
            return get_current_date(**args)
        if func == "get_current_time":
            return get_current_time(**args)
    if module == "people":
        return people_tools.call_function(func, args)
    raise ValueError(f"Function '{module}.{func}' not found")