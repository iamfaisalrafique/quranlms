from django.db import models
from django.core.exceptions import ValidationError

class HadithCollection(models.Model):
    """
    Represents a major Hadith collection (e.g., Sahih Bukhari).
    """
    slug = models.SlugField(unique=True, db_index=True)
    collection_id = models.IntegerField(null=True, blank=True)
    english_title = models.CharField(max_length=255)
    arabic_title = models.CharField(max_length=255)
    short_intro = models.TextField(blank=True)
    about = models.TextField(blank=True)
    num_hadith = models.IntegerField(default=0)
    total_hadith = models.IntegerField(default=0)
    has_books = models.BooleanField(default=True)
    has_chapters = models.BooleanField(default=True)
    status = models.CharField(max_length=50, default='complete')

    def __str__(self):
        return self.english_title


class HadithBook(models.Model):
    """
    Represents a book within a Hadith collection.
    """
    collection = models.ForeignKey(HadithCollection, on_delete=models.CASCADE, related_name='books')
    book_number = models.IntegerField(db_index=True)
    english_title = models.CharField(max_length=255)
    arabic_title = models.CharField(max_length=255)
    english_intro = models.TextField(blank=True)
    arabic_intro = models.TextField(blank=True)
    first_number = models.IntegerField(null=True, blank=True)
    last_number = models.IntegerField(null=True, blank=True)
    total_number = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default='complete')

    class Meta:
        unique_together = ('collection', 'book_number')

    def __str__(self):
        return f"{self.collection.slug} - Book {self.book_number}"


class HadithChapter(models.Model):
    """
    Represents a chapter within a Hadith book.
    """
    book = models.ForeignKey(HadithBook, on_delete=models.CASCADE, related_name='chapters')
    collection = models.ForeignKey(HadithCollection, on_delete=models.CASCADE)
    chapter_number = models.CharField(max_length=20)
    english_title = models.CharField(max_length=500)
    arabic_title = models.CharField(max_length=500)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['book', 'chapter_number'],
                name='unique_chapter_per_book',
            ),
            models.CheckConstraint(
                check=models.Q(collection=models.F('book__collection')),
                name='chapter_collection_matches_book',
            ),
        ]

    def clean(self):
        """
        Ensure that the chapter's collection matches the collection of its book.
        """
        # Only validate when both relations are set.
        if self.book_id is not None and self.collection_id is not None:
            if self.collection_id != self.book.collection_id:
                raise ValidationError(
                    {'collection': 'Chapter collection must match the collection of its book.'}
                )

    def __str__(self):
        return f"{self.collection.slug} - Book {self.book.book_number} - Chapter {self.chapter_number}"   


class Hadith(models.Model):
    """
    Represents an individual Hadith.
    """
    collection = models.ForeignKey(HadithCollection, on_delete=models.CASCADE, related_name='hadiths')    
    book = models.ForeignKey(HadithBook, on_delete=models.CASCADE, related_name='hadiths')
    chapter = models.ForeignKey(HadithChapter, on_delete=models.CASCADE, related_name='hadiths', null=True, blank=True)
    hadith_number = models.CharField(max_length=20, db_index=True)
    source_id = models.IntegerField(db_index=True)
    arabic_body = models.TextField()
    english_body = models.TextField()
    narrator = models.TextField(blank=True)
    grade = models.CharField(max_length=255, blank=True)
    reference = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('collection', 'source_id')
        ordering = ['collection', 'source_id']

    def __str__(self):
        return f"{self.collection.slug} - {self.hadith_number}"
