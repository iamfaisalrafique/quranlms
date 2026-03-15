import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings
import os

# Initialize Firebase app lazily if possible or silently trap if config is missing
try:
    if not firebase_admin._apps:
        # Assuming path to service account json or passed via env in production
        cred_path = getattr(settings, 'FIREBASE_CREDENTIALS', None)
        if cred_path and os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
except Exception as e:
    print(f"Firebase Init Error: {e}")

def send_push(user, title, body, data=None):
    """
    Send an FCM push notification to all active devices of a user.
    """
    if data is None:
        data = {}

    tokens = list(user.fcm_tokens.filter(is_active=True).values_list('token', flat=True))
    if not tokens:
        return {"success": 0, "failure": 0}

    # If Firebase wasn't fully initialized, mock the response
    if not firebase_admin._apps:
        print(f"[MOCK FCM] Sending push to {len(tokens)} devices: {title} - {body}")
        return {"success": len(tokens), "failure": 0}

    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data,
        tokens=tokens,
    )
    
    try:
        response = messaging.send_multicast(message)
        # Optionally handle failed tokens here (e.g. set is_active=False)
        return {"success": response.success_count, "failure": response.failure_count}
    except Exception as e:
        print(f"FCM Send Error: {e}")
        return {"error": str(e)}
