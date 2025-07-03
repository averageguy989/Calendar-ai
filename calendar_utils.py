# calendar_utils.py

from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from dateparser import parse
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Load service account credentials
SCOPES = ['https://www.googleapis.com/auth/calendar']

# ⬅️ Put your calendar ID here
CALENDAR_ID = os.getenv('CALENDAR_ID')  # e.g., aiassistantbot@group.calendar.google.com

service_account_info = json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"])

credentials = service_account.Credentials.from_service_account_info(
    service_account_info, scopes=SCOPES
)
service = build('calendar', 'v3', credentials=credentials)

# 🟢 Function to book a meeting
def book_appointment(summary, start_time, duration):
    print(summary, start_time, duration)

    # Step 1: Parse natural language into datetime
    start_dt = parse(start_time, settings={
        'TIMEZONE': 'Asia/Kolkata',
        'RETURN_AS_TIMEZONE_AWARE': True
    })

    if not start_dt:
        return "❌ Could not parse the start time."

    # Step 2: Compute end time
    end_dt = start_dt + timedelta(minutes=int(duration))

    # Step 3: Create Google Calendar event body
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_dt.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_dt.isoformat(),
            'timeZone': 'Asia/Kolkata',
        }
    }

    # Step 4: Call Google Calendar API
    event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return f"✅ Event created: {event.get('htmlLink')}"

# 🔵 Function to fetch existing events (for now)


# 🔵 Function to fetch events for a natural language date
def get_events(date):
    print(f"[🔍 Parsing date string]: {date}")

    # Use dateparser to convert natural language to datetime
    parsed_date = parse(date, settings={
        'TIMEZONE': 'Asia/Kolkata',
        'RETURN_AS_TIMEZONE_AWARE': True,
        'PREFER_DATES_FROM': 'future'
    })

    if not parsed_date:
        return "❌ Unable to parse the provided date."

    start = parsed_date.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    end = (parsed_date + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()

    print(f"[📅 Querying from]: {start} → {end}")

    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start,
        timeMax=end,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    event_list = [(e['start']['dateTime'], e['end']['dateTime']) for e in events if 'dateTime' in e['start']]
    if not event_list:
        return "No events found for this date."
    return f"Found {len(event_list)} events: {event_list}"