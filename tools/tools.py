from datetime import datetime
import tools.people.tools as people_tools
import tools.journals.tools as journals_tools
import tools.location.tools as location_tools

# https://platform.openai.com/docs/guides/function-calling
# If your function has no return value (e.g. send_email),
# simply return a string to indicate success or failure. (e.g. "success")

def get_current_date() -> str:
    """
    Get the current date and day of the week for temporal context.
    Use this when the someone asks about 'today', 'yesterday', 'tomorrow', or any time-related questions to ensure accurate date references.
    Returns:
        dict: The current date formatted as "YYYY-MM-DD" and "DayOfWeek Month DD, YYYY"
    """
    date = datetime.now().strftime("%Y-%m-%d")
    date_formatted = datetime.now().strftime("%A %B %d, %Y")
    return {
        "date": date,
        "date_formatted": date_formatted
    }

def get_current_time() -> str:
    """
    Get the current time for temporal context in conversations.
    Use this when the user asks about 'now', 'current time', or when time context is needed to provide accurate responses about timing, scheduling, or daily activities.
    Returns:
        dict: The current time formatted as "HH:MM" and "I:MM AM/PM"
    """
    time = datetime.now().strftime("%H:%M")
    time_formatted = datetime.now().strftime("%I:%M %p")
    return {
        "time": time,
        "time_formatted": time_formatted
    }

def call_function(name: str, args: dict):
    module, func = name.split("-")
    if module == "tools":
        if func == "get_current_date":
            return get_current_date(**args)
        if func == "get_current_time":
            return get_current_time(**args)
    if module == "people":
        return people_tools.call_function(func, args)
    if module == "journals":
        return journals_tools.call_function(func, args)
    if module == "location":
        return location_tools.call_function(func, args)
    raise ValueError(f"Function '{module}.{func}' not found")