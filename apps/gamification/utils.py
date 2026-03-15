from django.db.models import Count, Max
from .models import Badge, StudentBadge
from apps.lessons.models import LessonLog
from apps.quiz.models import QuizAttempt

def check_and_award_badges(student):
    """
    Check all badge conditions for a given student and award any that are newly met.
    Called after lesson log, quiz submission, or attendance update.
    """
    badges = Badge.objects.exclude(condition_type='manual')
    earned_badge_ids = set(student.earned_badges.values_list('badge_id', flat=True))
    
    # Pre-fetch required stats
    lesson_count = LessonLog.objects.filter(student=student).count()
    quiz_attempts = QuizAttempt.objects.filter(student=student, status='passed')
    quiz_count = quiz_attempts.count()
    max_quiz_score = quiz_attempts.aggregate(Max('score'))['score__max'] or 0
    current_streak = getattr(student, 'streak', None)
    streak_days = current_streak.current_streak if current_streak else 0
    
    # Note: khatam_count might need a field in LessonLog or StudentProfile. 
    # For now, we'll assume it's calculated or stored elsewhere.
    khatam_count = 0 

    for badge in badges:
        if badge.id in earned_badge_ids:
            continue
            
        is_met = False
        if badge.condition_type == 'lesson_count':
            is_met = lesson_count >= badge.condition_value
        elif badge.condition_type == 'streak_days':
            is_met = streak_days >= badge.condition_value
        elif badge.condition_type == 'quiz_count':
            is_met = quiz_count >= badge.condition_value
        elif badge.condition_type == 'quiz_score':
            is_met = max_quiz_score >= badge.condition_value
        elif badge.condition_type == 'khatam_count':
            is_met = khatam_count >= badge.condition_value
            
        if is_met:
            StudentBadge.objects.create(student=student, badge=badge)
