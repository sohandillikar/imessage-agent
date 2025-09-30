from datetime import datetime
import tools.people.tools as people_tools
import tools.journals.tools as journals_tools
import tools.location.tools as location_tools

# https://platform.openai.com/docs/guides/function-calling
# If your function has no return value (e.g. send_email),
# simply return a string to indicate success or failure. (e.g. "success")

def get_current_date_and_time() -> dict:
    """
    Get the current date and time for temporal context in conversations.
    Use this when someone asks about 'today', 'yesterday', 'tomorrow', 'now', 'current time', or any time-related questions to ensure accurate date and time references.
    Returns:
        dict: The current date and time with the following keys:
            - date: Date formatted as "YYYY-MM-DD"
            - date_formatted: Date formatted as "DayOfWeek Month DD, YYYY"
            - time: Time formatted as "HH:MM" (24-hour format)
            - time_formatted: Time formatted as "I:MM AM/PM" (12-hour format)
    """
    now = datetime.now()
    return {
        "date": now.strftime("%Y-%m-%d"),
        "date_formatted": now.strftime("%A %B %d, %Y"),
        "time": now.strftime("%H:%M"),
        "time_formatted": now.strftime("%I:%M %p")
    }

def call_function(name: str, args: dict):
    module, func = name.split("-")
    if module == "tools":
        if func == "get_current_date_and_time":
            return get_current_date_and_time(**args)
    if module == "people":
        return people_tools.call_function(func, args)
    if module == "journals":
        return journals_tools.call_function(func, args)
    if module == "location":
        return location_tools.call_function(func, args)
    raise ValueError(f"Function '{module}.{func}' not found")