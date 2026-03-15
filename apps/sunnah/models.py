from django.db import models

class HadithCollection(models.Model):
    """Major Hadith Collection (e.g., Bukhari, Muslim)."""
    slug = models.SlugField(unique=True, help_text="Collection identifier (e.g. bukhari)")
    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255)
    total_hadiths = models.PositiveIntegerField(default=0)
    introduction_en = models.TextField(blank=True)

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.name_en


class HadithBook(models.Model):
    """Book within a Hadith collection."""
    collection = models.ForeignKey(HadithCollection, on_delete=models.CASCADE, related_name='books')
    book_number = models.CharField(max_length=20)
    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255)

    class Meta:
        ordering = ['collection', 'book_number']
        unique_together = ('collection', 'book_number')

    def __str__(self):
        return f"{self.collection.name_en} - Book {self.book_number}: {self.name_en}"


class HadithChapter(models.Model):
    """Chapter within a Hadith book."""
    book = models.ForeignKey(HadithBook, on_delete=models.CASCADE, related_name='chapters')
    chapter_number = models.CharField(max_length=20)
    title_en = models.CharField(max_length=500)
    title_ar = models.CharField(max_length=500)

    class Meta:
        ordering = ['book', 'chapter_number']
        unique_together = ('book', 'chapter_number')

    def __str__(self):
        return f"Chapter {self.chapter_number}: {self.title_en}"


class Hadith(models.Model):
    """Individual Hadith narration."""
    chapter = models.ForeignKey(HadithChapter, on_delete=models.CASCADE, related_name='hadiths')
    hadith_number = models.CharField(max_length=20)
    reference_inbook = models.CharField(max_length=100, blank=True)
    arabic_text = models.TextField(help_text="Amiri Font recommended")
    text_en = models.TextField()
    text_ur = models.TextField(blank=True)
    narrator_en = models.CharField(max_length=500, blank=True)
    grade = models.CharField(max_length=255, blank=True)
    grade_source = models.CharField(max_length=255, blank=True)
    urn = models.CharField(max_length=100, unique=True, help_text="Unique Research Number from Sunnah.com")

    class Meta:
        ordering = ['chapter', 'hadith_number']

    def __str__(self):
        return f"Hadith {self.hadith_number} in {self.chapter.book.collection.name_en}"
