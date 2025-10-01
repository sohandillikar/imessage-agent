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

def create_event(title: str, description: str, start: str, end: str, location: str = None) -> str:
    """
    Use this to add a new event to your calendar only after plans are confirmed in conversation.
    IMPORTANT: Use tools-get_current_date_and_time to get a reference date and time.
    Args:
        title: The title of the event
        description: The description of the event
        start: The start date and time of the event in YYYY-MM-DD HH:MM format
        end: The end date and time of the event in YYYY-MM-DD HH:MM format
        location: The location of the event, if mentioned
    Returns:
        str: Status of the update operation (e.g. "success", "error")
    """
    start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M")
    event_start = gcal_utils.tz.localize(start_dt).isoformat()
    event_end =  gcal_utils.tz.localize(end_dt).isoformat()
    calendar = gcal_utils.get_calendar_by_name("iMessage Agent")
    event = gcal_utils.create_event(calendar["id"], title, event_start, event_end, description, location)
    print(f"Created new calendar event: {event['summary']}")
    return "success"

def call_function(name: str, args: dict):
    if name == "get_schedule":
        return get_schedule(**args)
    if name == "create_event":
        return create_event(**args)
    raise ValueError(f"Function 'gcal.{name}' not found")