import tools.gcal.utils as gcal_utils
from datetime import datetime, time, timedelta

def get_schedule(date: str) -> list:
    """
    Get a list of tasks and events you have planned for any day.
    Use this when someone asks about your day, plans, availability, or when trying to schedule tasks, events, activities, or plans.
    Use this instead of the file_search tool when a specific day is being discussed.
    IMPORTANT: Use tools-get_current_date_and_time to get a reference date.
    Args:
        date: The date to get a list of tasks and events for in YYYY-MM-DD format
    Returns:
        list: A list of tasks and events you have planned
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
    Use this to schedule any task, plan, event, activity, or reminder that is being discussed in conversation.
    IMPORTANT:
        - Use tools-get_current_date_and_time to get a reference date and time.
        - Use gcal-get_schedule to ensure that you are available at the time of the event and that a similar event is not already scheduled. If a similar event is already scheduled, use gcal-modify_event to modify the event.
    Args:
        title: The title of the event
        description: The description of the event
        start: The start date and time of the event in YYYY-MM-DD HH:MM format
        end: The end date and time of the event in YYYY-MM-DD HH:MM format
        location: The location of the event, if mentioned
    Returns:
        str: ID of the created event
    """
    start_dt = datetime.strptime(start[:16], "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(end[:16], "%Y-%m-%d %H:%M")
    event_start = gcal_utils.tz.localize(start_dt).isoformat()
    event_end =  gcal_utils.tz.localize(end_dt).isoformat()
    calendar = gcal_utils.get_calendar_by_name("iMessage Agent")
    event = gcal_utils.create_event(calendar["id"], title, event_start, event_end, description, location)
    return event["id"]

def modify_event(event_id: str, title: str = None, description: str = None, start: str = None, end: str = None, location: str = None) -> str:
    """
    Use this to modify any task, plan, event, activity, or reminder that is being discussed in conversation.
    IMPORTANT:
        - Use tools-get_current_date_and_time to get a reference date and time.
        - Use gcal-get_schedule to get the id of the event you want to modify.
    Args:
        event_id: The id from gcal-get_schedule of the event you want to modify
        title: The title of the event
        description: The description of the event
        start: The start date and time of the event in YYYY-MM-DD HH:MM format
        end: The end date and time of the event in YYYY-MM-DD HH:MM format
        location: The location of the event
    Returns:
        str: Status of the update operation (e.g. "success", "error")
    """
    if start:
        start_dt = datetime.strptime(start[:16], "%Y-%m-%d %H:%M")
        start = gcal_utils.tz.localize(start_dt).isoformat()
    if end:
        end_dt = datetime.strptime(end[:16], "%Y-%m-%d %H:%M")
        end = gcal_utils.tz.localize(end_dt).isoformat()
    calendar = gcal_utils.get_calendar_by_name("iMessage Agent")
    try:
        gcal_utils.modify_event(calendar["id"], event_id, title, description, start, end, location)
    except:
        return "Error: This event is mandatory and cannot be modified"
    return "success"

def delete_event(event_id: str) -> str:
    """
    Use this to delete any task, plan, event, activity, or reminder that gets cancelled in conversation.
    IMPORTANT:
        - Use tools-get_current_date_and_time to get a reference date and time.
        - Use gcal-get_schedule to get the id of the event you want to delete.
    Args:
        event_id: The id from gcal-get_schedule of the event you want to delete
    Returns:
        str: Status of the delete operation (e.g. "success", "error")
    """
    calendar = gcal_utils.get_calendar_by_name("iMessage Agent")
    try:
        gcal_utils.delete_event(calendar["id"], event_id)
    except:
        return "Error: This event is mandatory and cannot be deleted"
    return "success"

def call_function(name: str, args: dict):
    if name == "get_schedule":
        return get_schedule(**args)
    if name == "create_event":
        return create_event(**args)
    if name == "modify_event":
        return modify_event(**args)
    if name == "delete_event":
        return delete_event(**args)
    raise ValueError(f"Function 'gcal.{name}' not found")