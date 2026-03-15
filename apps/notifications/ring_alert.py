import os
import uuid
from django.conf import settings
from gtts import gTTS
from django.utils import timezone
from .models import RingAlertLog
from .fcm import send_push

def generate_audio(text, lang='en'):
    """Generates an mp3 file from text using gTTS."""
    tts = gTTS(text=text, lang=lang)
    
    # Ensure directory exists
    alerts_dir = os.path.join(settings.MEDIA_ROOT, 'ring_alerts')
    if not os.path.exists(alerts_dir):
        os.makedirs(alerts_dir)
        
    filename = f"alert_{uuid.uuid4().hex[:10]}.mp3"
    filepath = os.path.join(alerts_dir, filename)
    tts.save(filepath)
    
    return f"{settings.MEDIA_URL}ring_alerts/{filename}"

def send_ring_alert(teacher, student, message="Please join the class now."):
    """
    Generates an audio message and sends a silent push notification 
    with the audio URL to the student's devices.
    """
    audio_url = generate_audio(message)
    
    # Send FCM silent push data payload
    push_data = {
        "type": "ring_alert",
        "audio_url": audio_url,
        "message": message,
        "teacher_name": teacher.user.get_full_name()
    }
    
    # Create log entry
    log_entry = RingAlertLog.objects.create(
        teacher=teacher,
        student=student,
        message=message,
        audio_url=audio_url
    )
    
    response = send_push(
        user=student.user,
        title="Class Alert",
        body=message,
        data=push_data
    )
    
    if response and response.get('success', 0) > 0:
        log_entry.delivered = True
        log_entry.save()
        
    return log_entry
