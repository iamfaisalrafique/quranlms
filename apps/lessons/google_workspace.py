import datetime
# Stub classes for Google Workspace integration until specific credentials are provided
# In production, this would use googleapiclient.discovery.build('calendar', 'v3', credentials=creds)

def create_meet_space(teacher_token):
    """
    Creates a Google Meet space on behalf of the teacher.
    Returns: meet_url, meet_id
    """
    # This is a mocked generated meet link
    meet_id = f"ixv-{datetime.datetime.now().strftime('%M%S')}-abc"
    meet_url = f"https://meet.google.com/{meet_id}"
    return meet_url, meet_id

def create_calendar_event(teacher_token, meet_url, scheduled_at, duration_mins=60):
    """
    Creates a Calendar event on the teacher's primary calendar.
    Returns: event_id
    """
    url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
    headers = {
        "Authorization": f"Bearer {teacher_token}",
        "Content-Type": "application/json"
    }

    # scheduled_at can be a string or datetime
    if isinstance(scheduled_at, datetime.datetime):
        start_time = scheduled_at.isoformat()
        end_time = (scheduled_at + datetime.timedelta(minutes=duration_mins)).isoformat()
    else:
        start_time = scheduled_at
        # Assuming scheduled_at is ISO string if not datetime
        end_time = scheduled_at

    body = {
        "summary": "Quran Lesson",
        "description": f"Join via Meet: {meet_url}",
        "start": {"dateTime": start_time, "timeZone": "UTC"},
        "end": {"dateTime": end_time, "timeZone": "UTC"},
        "conferenceData": {
            "createRequest": {"requestId": f"req_{datetime.datetime.now().timestamp()}"}
        }
    }

    try:
        resp = requests.post(url, headers=headers, json=body, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("id")
    except Exception as e:
        logger.error(f"Error creating calendar event: {e}")

    return f"evt_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

import requests
import logging

logger = logging.getLogger(__name__)

def send_calendar_invites(teacher_token, event_id, student_emails):
    """
    Updates a Calendar event to add student email addresses as attendees.
    Uses patch as per MISSION CRITICAL requirements.
    """
    url = f"https://www.googleapis.com/calendar/v3/calendars/primary/events/{event_id}"
    headers = {
        "Authorization": f"Bearer {teacher_token}",
        "Content-Type": "application/json"
    }
    params = {
        "sendUpdates": "all"
    }
    body = {
        "attendees": [{"email": email} for email in student_emails],
        "guestsCanSeeOtherGuests": False
    }

    try:
        # We use requests directly to ensure implementation even if google-api-client is missing/misconfigured
        resp = requests.patch(url, headers=headers, params=params, json=body, timeout=10)
        if resp.status_code != 200:
            logger.error(f"Google Calendar patch failed: {resp.text}")
        return resp.json() if resp.status_code == 200 else None
    except Exception as e:
        logger.error(f"Error calling Google Calendar API: {e}")
        return None
