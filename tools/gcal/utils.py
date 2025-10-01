import os
from pytz import timezone
from datetime import datetime
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

tz_env_var = os.getenv("TIMEZONE")
if not tz_env_var:
    raise ValueError("TIMEZONE environment variable is not set")
tz = timezone(tz_env_var)

# If modifying these scopes, delete token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_gcal_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("calendar", "v3", credentials=creds)
        return service
    except HttpError as error:
        print(f"An HttpError occurred: {error}")

service = get_gcal_service()

def get_all_calendars():
    calendars = service.calendarList().list().execute()["items"]
    return calendars

def get_calendar_by_name(name: str):
    calendars = get_all_calendars()
    for calendar in calendars:
        if calendar["summary"] == name:
            return calendar
    return None

def create_calendar(name: str, description: str, time_zone: str = os.getenv("TIMEZONE")):
    new_calendar = service.calendars().insert(body={
        "summary": name,
        "description": description,
        "timeZone": time_zone
    }).execute()
    return new_calendar

def create_event(calendar_id: str, title: str, start: str, end: str, description: str = None, location: str = None):
    event = {
        "summary": title,
        "start": {"dateTime": start, "timeZone": tz_env_var},
        "end": {"dateTime": end, "timeZone": tz_env_var}
    }
    if description:
        event["description"] = description
    if location:
        event["location"] = location
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return event

def modify_event(calendar_id: str, event_id: str, title: str = None, description: str = None, start: str = None, end: str = None, location: str = None):
    updates = {}
    if title:
        updates["summary"] = title
    if description:
        updates["description"] = description
    if start:
        updates["start"] = {"dateTime": start, "timeZone": tz_env_var}
    if end:
        updates["end"] = {"dateTime": end, "timeZone": tz_env_var}
    if location:
        updates["location"] = location
    event = service.events().patch(calendarId=calendar_id, eventId=event_id, body=updates).execute()
    return event

def is_event_confirmed(event: dict):
    if "attendees" in event:
        self_status = [a["responseStatus"] for a in event["attendees"] if a.get("self", False)]
        if self_status and self_status[0] != "accepted":
            return False
    return True

def get_events_from_calendar(calendar_id: str, start: str, end: str, confirmed_only: bool = False):
    events = service.events().list(
        calendarId=calendar_id,
        timeMin=start,
        timeMax=end,
        singleEvents=True,
        orderBy='startTime'
    ).execute()["items"]
    if confirmed_only:
        return [e for e in events if is_event_confirmed(e)]
    return events

def get_events_from_calendars(calendars: list[dict], start: str, end: str, confirmed_only: bool = False):
    all_events = []
    for calendar in calendars:
        calendar_events = get_events_from_calendar(calendar["id"], start, end, confirmed_only=confirmed_only)
        all_events.extend(calendar_events)
    return all_events

def extract_key_info_from_event(event: dict):
    return {
        "id": event["id"],
        "title": event["summary"],
        "description": event.get("description", None),
        "location": event.get("location", None),
        "start": datetime.fromisoformat(event["start"]["dateTime"]).strftime("%Y-%m-%d %H:%M:%S"),
        "end": datetime.fromisoformat(event["end"]["dateTime"]).strftime("%Y-%m-%d %H:%M:%S"),
        "status": "confirmed" if is_event_confirmed(event) else "not confirmed"
    }

def extract_key_info_from_events(events: list[dict]):
    return [extract_key_info_from_event(e) for e in events]