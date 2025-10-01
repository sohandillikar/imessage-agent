import tools.gcal.utils as gcal_utils
from datetime import datetime, time, timedelta

def get_schedule(date: str) -> list:
    """
    Get a list of events you have planned for any day.
    Use this when someone asks about your day, plans, availability, or when trying to schedule events/activities.
    Use this instead of the file_search tool when a specific day is being discussed.
    IMPORTANT: Use tools-get_current_date_and_time to get a reference date.
    Args:
        date: The date to get a list of events for in YYYY-MM-DD format
    Returns:
        list: A list of events you have planned
    """
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    start = gcal_utils.tz.localize(datetime.combine(date_obj, time.min))
    end = start + timedelta(days=1)
    start = start.isoformat()
    end = end.isoformat()
    calendars = gcal_utils.get_all_calendars()
    events = gcal_utils.get_events_from_calendars(calendars, start, end, confirmed_only=True)
    events = gcal_utils.extract_key_info_from_events(events)
    return events

def call_function(name: str, args: dict):
    if name == "get_schedule":
        return get_schedule(**args)
    raise ValueError(f"Function 'gcal.{name}' not found")