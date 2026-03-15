from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.attendance.models import AttendanceStreak, AttendanceRecord
from apps.gamification.utils import check_and_award_badges

class Command(BaseCommand):
    help = 'Updates student attendance streaks and grace days.'

    def handle(self, *args, **options):
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        streaks = AttendanceStreak.objects.all()
        
        for streak in streaks:
            student = streak.student
            # Check if student attended yesterday
            attended_yesterday = AttendanceRecord.objects.filter(
                student=student,
                date=yesterday,
                status='present'
            ).exists()
            
            if attended_yesterday:
                # If they already updated for yesterday, skip
                if streak.last_attendance_date == yesterday:
                    continue
                
                # Check if they attended or used grace the day before yesterday
                day_before = yesterday - timedelta(days=1)
                if streak.last_attendance_date == day_before:
                    streak.current_streak += 1
                else:
                    # Streak was broken before yesterday
                    streak.current_streak = 1
                
                streak.last_attendance_date = yesterday
                
                # Award grace day every 7 days
                if streak.current_streak % 7 == 0:
                    if streak.grace_days_banked < streak.grace_days_allowed:
                        streak.grace_days_banked += 1
                
                # Update longest streak
                if streak.current_streak > streak.longest_streak:
                    streak.longest_streak = streak.current_streak
                    
            else:
                # Did not attend yesterday
                if streak.last_attendance_date == yesterday:
                    # Already processed yesterday as attended? (Maybe multiple runs)
                    continue
                    
                if streak.current_streak > 0:
                    if streak.grace_days_banked > 0:
                        streak.grace_days_banked -= 1
                        streak.grace_days_used += 1
                        # We treat this as "attended" virtually to keep streak alive
                        streak.last_attendance_date = yesterday
                    else:
                        streak.current_streak = 0
            
            streak.save()
            # Check for streak-based badges
            check_and_award_badges(student)
            
        self.stdout.write(self.style.SUCCESS('Successfully updated streaks.'))
