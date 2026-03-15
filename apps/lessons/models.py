from django.db import models
from django.conf import settings

class QuranBookmark(models.Model):
    """Student bookmarks for Quranic ayats."""
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE, related_name='quran_bookmarks')
    ayat = models.ForeignKey('quran.Ayat', on_delete=models.CASCADE, related_name='bookmarks')
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'ayat')
        ordering = ['-created_at']

    def __str__(self):
        return f"Bookmark by {self.student.user.username} for {self.ayat.verse_key}"


class HadithBookmark(models.Model):
    """Student bookmarks for Hadiths."""
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE, related_name='hadith_bookmarks')
    hadith = models.ForeignKey('sunnah.Hadith', on_delete=models.CASCADE, related_name='bookmarks')
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'hadith')
        ordering = ['-created_at']

    def __str__(self):
        return f"Hadith Bookmark by {self.student.user.username} for {self.hadith.urn}"


class LessonType(models.TextChoices):
    QURAN_RECITATION = 'quran_recitation', 'Quran Recitation'
    QURAN_MEMORIZATION = 'quran_memorization', 'Quran Memorization'
    QURAN_REVISION = 'quran_revision', 'Quran Revision'
    TAJWEED = 'tajweed', 'Tajweed'
    TAFSIR = 'tafsir', 'Tafsir'
    ISLAMIC_STUDIES = 'islamic_studies', 'Islamic Studies'
    ARABIC_LANGUAGE = 'arabic_language', 'Arabic Language'
    DUA_HADITH = 'dua_hadith', 'Dua & Hadith'


class LessonLog(models.Model):
    """Core academic logging for each lesson session."""
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE, related_name='lesson_logs')
    teacher = models.ForeignKey('accounts.TeacherProfile', on_delete=models.CASCADE, related_name='lesson_logs')
    lesson_type = models.CharField(max_length=50, choices=LessonType.choices)
    date = models.DateField(auto_now_add=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    
    # Quran specific fields (optional if lesson is not Quran related)
    surah_from = models.PositiveIntegerField(null=True, blank=True)
    ayat_from = models.PositiveIntegerField(null=True, blank=True)
    surah_to = models.PositiveIntegerField(null=True, blank=True)
    ayat_to = models.PositiveIntegerField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(default=5, help_text="Rating 1-5")
    
    homework_given = models.BooleanField(default=False)
    homework_description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.lesson_type} - {self.student.user.get_full_name()} ({self.date})"


class ClassSession(models.Model):
    """Scheduled class sessions (can be one-to-one or group)."""
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        LIVE = 'live', 'Live'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    teacher = models.ForeignKey('accounts.TeacherProfile', on_delete=models.CASCADE, related_name='class_sessions')
    students = models.ManyToManyField('accounts.StudentProfile', related_name='class_sessions')
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=30)
    
    google_meet_url = models.URLField(blank=True, null=True)
    google_meet_id = models.CharField(max_length=100, blank=True, null=True)
    google_calendar_event_id = models.CharField(max_length=255, blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    recording_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['scheduled_at']

    def __str__(self):
        return f"Session with {self.teacher.user.username} @ {self.scheduled_at}"
