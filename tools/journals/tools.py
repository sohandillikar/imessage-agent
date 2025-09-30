import tools.journals.utils as journals_utils

def get_day_overview(date: str):
    """
    Get an overview of any day that includes your thoughts, feelings, plans, events, people you interacted with, and topics you discussed.
    Use this when someone asks anything about you, how you're doing, your day, plans, thoughts, feelings, interactions, etc.
    When querying for a specific day, use this instead of file search.
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
        # del latest_journal["date"]
        del latest_journal["date_formatted"]
        return latest_journal
    return None

def call_function(name: str, args: dict):
    if name == "get_day_overview":
        return get_day_overview(**args)
    raise ValueError(f"Function 'journals.{name}' not found")