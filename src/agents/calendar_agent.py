# src/agents/calendar_agent.py
import os
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tzlocal import get_localzone_name # <-- ADDED: Import to get local timezone

load_dotenv()


SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar"
]


class CalendarAgent:
    """Creates Google Calendar events for completed reports.
    
    Requires OAuth credentials with Calendar scope.
    Creates events in the primary calendar by default.
    """

    def __init__(self, credentials_path: str = "credentials.json", token_path: str = "token.json"):
        self.credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH", credentials_path)
        self.token_path = os.getenv("GOOGLE_TOKEN_PATH", token_path)

    def _get_service(self):
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Google OAuth client secrets not found at {self.credentials_path}."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_path, "w") as token:
                token.write(creds.to_json())
        return build("calendar", "v3", credentials=creds)

    def create_report_event(
        self, 
        report_name: str, 
        generation_time: datetime,
        calendar_id: Optional[str] = None
    ) -> Optional[str]:
        """Creates a calendar event for the completed report."""
        try:
            service = self._get_service()
            
            # Use primary calendar if none specified
            if not calendar_id:
                calendar_id = "primary"
            
            # --- MODIFICATION START ---
            
            # Get the system's local timezone name (e.g., 'Asia/Kolkata')
            local_timezone = get_localzone_name()
            
            # Create event details
            event = {
                "summary": f"📄 Report Completed: {report_name}",
                "description": f"Research digest report '{report_name}' has been generated and is ready for review.",
                "start": {
                    "dateTime": generation_time.isoformat(),
                    "timeZone": local_timezone,  # <-- CHANGED: Use local timezone
                },
                "end": {
                    "dateTime": (generation_time + timedelta(minutes=30)).isoformat(),
                    "timeZone": local_timezone,  # <-- CHANGED: Use local timezone
                },
                # <-- REMOVED: The entire "reminders" block has been deleted
            }
            
            # --- MODIFICATION END ---
            
            event = service.events().insert(
                calendarId=calendar_id, 
                body=event
            ).execute()
            
            event_id = event.get("id")
            event_link = event.get("htmlLink")
            print(f"✅ Calendar event created. Event ID: {event_id}")
            print(f"   📅 View event: {event_link}")
            
            return event_id
            
        except Exception as e:
            print(f"❌ Failed to create calendar event: {e}")
            return None