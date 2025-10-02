import tools.journals.utils as journals_utils

def get_day_overview(date: str) -> dict:
    """
    Get an overview of any day that includes your thoughts, feelings, plans, priorities, people you interacted with, and topics you discussed.
    Use this when someone asks about:
        - You, how you're doing, or your day
        - Your morning, afternoon, evening, or night
        - Your plans/priorities for any day
        - Your thoughts or feelings
    Use this instead of the file_search tool when a specific day is being discussed.
    IMPORTANT: Use tools-get_current_date_and_time to get a reference date.
    Args:
        date: The date to get the overview for in YYYY-MM-DD format
    Returns:
        dict: An overview of the day
    """
    journals = journals_utils.get_journals()
    relevant_journals = [j for j in journals if j["date"].startswith(date)]
    if relevant_journals:
        latest_date = max([j["date"] for j in relevant_journals])
        latest_journal = [j for j in relevant_journals if j["date"] == latest_date][0]
        del latest_journal["title"]
        del latest_journal["date_formatted"]
        return latest_journal
    return None

def call_function(name: str, args: dict):
    if name == "get_day_overview":
        return get_day_overview(**args)
    raise ValueError(f"Function 'journals.{name}' not found")