from django.core.management.base import BaseCommand
from apps.gamification.models import Badge

class Command(BaseCommand):
    help = 'Seeds default badges for the IslamicLMS system.'

    def handle(self, *args, **options):
        badges = [
            {
                "name": "First Lesson",
                "description": "Completed your first lesson log!",
                "icon": "📖",
                "condition_type": "lesson_count",
                "condition_value": 1
            },
            {
                "name": "7-Day Streak",
                "description": "Attended classes for 7 consecutive days.",
                "icon": "🔥",
                "condition_type": "streak_days",
                "condition_value": 7
            },
            {
                "name": "30-Day Streak",
                "description": "Attended classes for 30 consecutive days.",
                "icon": "🏆",
                "condition_type": "streak_days",
                "condition_value": 30
            },
            {
                "name": "10 Quizzes",
                "description": "Successfully completed 10 quizzes.",
                "icon": "🧠",
                "condition_type": "quiz_count",
                "condition_value": 10
            },
            {
                "name": "Perfect Score",
                "description": "Got 100% on a quiz.",
                "icon": "💎",
                "condition_type": "quiz_score",
                "condition_value": 100
            },
            {
                "name": "100 Lessons",
                "description": "Milestone: Completed 100 lessons.",
                "icon": "⭐",
                "condition_type": "lesson_count",
                "condition_value": 100
            },
            {
                "name": "Quran Khatam",
                "description": "Completed a full Quran Khatam.",
                "icon": "🕌",
                "condition_type": "khatam_count",
                "condition_value": 1
            },
            {
                "name": "Top Student",
                "description": "Awarded for exceptional performance.",
                "icon": "👑",
                "condition_type": "manual",
                "condition_value": 1
            },
        ]

        for b_data in badges:
            badge, created = Badge.objects.get_or_create(
                name=b_data['name'],
                defaults={
                    'description': b_data['description'],
                    'icon': b_data['icon'],
                    'condition_type': b_data['condition_type'],
                    'condition_value': b_data['condition_value']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created badge: {badge.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Badge already exists: {badge.name}'))
