from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.lessons.models import ClassSession
from apps.notifications.fcm import send_push

class Command(BaseCommand):
    help = 'Sends class reminders via FCM to students 15 minutes before the session starts.'

    def handle(self, *args, **options):
        now = timezone.now()
        upcoming_window = now + timedelta(minutes=15)
        
        # Find scheduled classes starting within the next 15-16 minutes
        upcoming_sessions = ClassSession.objects.filter(
            status='scheduled',
            scheduled_at__gt=now,
            scheduled_at__lte=upcoming_window
        ).prefetch_related('students__user')
        
        count = 0
        for session in upcoming_sessions:
            teacher_name = session.teacher.user.get_full_name()
            time_str = session.scheduled_at.strftime("%I:%M %p")
            
            title = f"Upcoming Class with {teacher_name}"
            body = f"Your class is starting at {time_str}. Please be ready!"
            data = {"type": "class_reminder", "session_id": str(session.id), "meet_url": session.google_meet_url}
            
            for student in session.students.all():
                send_push(student.user, title, body, data)
                count += 1
                
                # Note: WhatsApp reminder to guardian (Growth+ tier logic)
                # would be evaluated and dispatched here.
                
            # Optionally mark session as 'notified' if desired to avoid duplicates
            
        self.stdout.write(self.style.SUCCESS(f'Successfully sent {count} class reminders.'))
