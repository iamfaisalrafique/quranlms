import os
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def generate_achievement_certificate(student, academy, achievement_text, teacher_name):
    """
    Renders a certificate PDF for a student.
    """
    try:
        from weasyprint import HTML
    except ImportError:
        HTML = None
        print("WeasyPrint is not installed or configured correctly.")
    context = {
        'student_name': student.user.get_full_name(),
        'academy_name': academy.name,
        'achievement': achievement_text,
        'teacher_name': teacher_name,
        'date': timezone.now().strftime('%B %d, %Y'),
    }
    
    html_string = render_to_string('reports/certificate.html', context)
    
    if HTML:
        pdf_file = HTML(string=html_string).write_pdf()
    else:
        # Fallback for dev environment without WeasyPrint
        pdf_file = html_string.encode('utf-8')
    
    filename = f"certificate_{student.student_id}_{timezone.now().strftime('%Y%m%d%H%M%S')}.pdf"
    path = f"reports/certificates/{filename}"
    
    storage_path = default_storage.save(path, ContentFile(pdf_file))
    return default_storage.url(storage_path)
