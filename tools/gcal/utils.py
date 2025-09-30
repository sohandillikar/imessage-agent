import os
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
        "title": event["summary"],
        "description": event.get("description", None),
        "location": event.get("location", None),
        "start": datetime.fromisoformat(event["start"]["dateTime"]).strftime("%Y-%m-%d %H:%M:%S"),
        "end": datetime.fromisoformat(event["end"]["dateTime"]).strftime("%Y-%m-%d %H:%M:%S"),
        "status": "confirmed" if is_event_confirmed(event) else "not confirmed"
    }

def extract_key_info_from_events(events: list[dict]):
    return [extract_key_info_from_event(e) for e in events]