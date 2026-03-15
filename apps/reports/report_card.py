from django.utils import timezone
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from apps.attendance.models import AttendanceRecord, AttendanceStreak
from apps.quiz.models import QuizAttempt
from apps.lessons.models import LessonLog
from apps.ai.router import AIRouter

def generate_student_report_card(student):
    """
    Collects student stats and generates a report card PDF.
    """
    try:
        from weasyprint import HTML
    except ImportError:
        HTML = None
        print("WeasyPrint is not installed or configured correctly.")
    # 1. Collect Stats
    total_classes = AttendanceRecord.objects.filter(student=student).count()
    present_classes = AttendanceRecord.objects.filter(student=student, status='present').count()
    attendance_pct = (present_classes / total_classes * 100) if total_classes > 0 else 0
    
    quiz_attempts = QuizAttempt.objects.filter(student=student, status__in=['passed', 'failed'])
    quiz_avg = sum([q.score for q in quiz_attempts]) / quiz_attempts.count() if quiz_attempts.count() > 0 else 0
    
    lesson_count = LessonLog.objects.filter(student=student).count()
    
    try:
        streak_obj = student.streak
        current_streak = streak_obj.current_streak
    except:
        current_streak = 0
        
    badges = student.earned_badges.select_related('badge')
    
    # 2. Get AI Remarks
    router = AIRouter()
    topic = f"performance of student {student.user.get_full_name()} with {attendance_pct}% attendance and {quiz_avg}% quiz average"
    prompt = f"Write a 2-sentence encouraging and professional teacher remark about the {topic}."
    
    try:
        ai_response = router.model.generate_content(prompt)
        teacher_remarks = ai_response.text.strip()
    except:
        teacher_remarks = "The student is making steady progress. Keep up the good work!"

    context = {
        'student': student,
        'attendance_pct': round(attendance_pct, 1),
        'quiz_avg': round(quiz_avg, 1),
        'lesson_count': lesson_count,
        'current_streak': current_streak,
        'badges': badges,
        'teacher_remarks': teacher_remarks,
        'date': timezone.now().strftime('%B %d, %Y'),
    }
    
    html_string = render_to_string('reports/report_card.html', context)
    
    if HTML:
        pdf_file = HTML(string=html_string).write_pdf()
    else:
        pdf_file = html_string.encode('utf-8')
    
    filename = f"report_card_{student.student_id}_{timezone.now().strftime('%Y%m%d%H%M%S')}.pdf"
    path = f"reports/report_cards/{filename}"
    
    storage_path = default_storage.save(path, ContentFile(pdf_file))
    return default_storage.url(storage_path)
