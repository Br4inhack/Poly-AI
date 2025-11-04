"""
Google Calendar integration.
Uses OAuth 2.0 installed app flow storing token.json.
"""
from __future__ import annotations
from datetime import datetime
from typing import Dict, Any, Optional

import config

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def _build_service():
    # On Streamlit Cloud, write credentials/token from secrets if provided
    try:
        config.write_google_oauth_files_from_secrets()
    except Exception:
        pass
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = None
    if config.GOOGLE_TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(config.GOOGLE_TOKEN_FILE), SCOPES)
        except Exception:
            creds = None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
        if not creds:
            if not config.GOOGLE_CREDENTIALS_FILE.exists():
                raise FileNotFoundError("Google credentials.json not found. See README for setup.")
            flow = InstalledAppFlow.from_client_secrets_file(str(config.GOOGLE_CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        config.GOOGLE_TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    service = build("calendar", "v3", credentials=creds)
    return service


def create_event(summary: str, start: datetime, end: datetime, timezone: Optional[str] = None) -> Dict[str, Any]:
    tz = timezone or config.DEFAULT_TIMEZONE
    service = _build_service()
    event = {
        "summary": summary[:200],
        "start": {"dateTime": start.isoformat(), "timeZone": tz},
        "end": {"dateTime": end.isoformat(), "timeZone": tz},
    }
    try:
        created = service.events().insert(calendarId=config.GOOGLE_CALENDAR_ID, body=event).execute()
        html_link = created.get("htmlLink")
        return {"success": True, "message": f"Event created: {html_link}", "data": created}
    except Exception as e:
        return {"success": False, "message": f"Google Calendar error: {e}"}
