from django.db import models


class Surah(models.Model):
    """Quranic Surah (Chapter) metadata."""
    number = models.PositiveIntegerField(unique=True, help_text="Surah number (1-114)")
    name_arabic = models.CharField(max_length=255)
    name_english = models.CharField(max_length=255)
    name_transliteration = models.CharField(max_length=255)
    revelation_type = models.CharField(max_length=20, choices=[('Meccan', 'Meccan'), ('Medinan', 'Medinan')])
    ayat_count = models.PositiveIntegerField()
    juz_start = models.PositiveIntegerField()
    page_start = models.PositiveIntegerField()
    chronological_order = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"{self.number}. {self.name_english}"


class Ayat(models.Model):
    """Quranic Ayat (Verse) metadata and translations."""
    surah = models.ForeignKey(Surah, on_delete=models.CASCADE, related_name='ayats')
    number = models.PositiveIntegerField(help_text="Ayat number within the surah")
    arabic_text = models.TextField(help_text="KFGQPC Uthmanic Script")
    translation_en = models.TextField(help_text="Mustafa Khattab")
    translation_ur = models.TextField()
    transliteration = models.TextField()
    juz = models.PositiveIntegerField()
    page = models.PositiveIntegerField()
    sajda = models.BooleanField(default=False)
    ruku = models.PositiveIntegerField()
    hizb = models.PositiveIntegerField()
    verse_key = models.CharField(max_length=20, unique=True, help_text="e.g. 1:1")

    class Meta:
        ordering = ['surah__number', 'number']
        unique_together = ('surah', 'number')

    def __str__(self):
        return self.verse_key


class AyatWord(models.Model):
    """Word-by-word data for an Ayat."""
    ayat = models.ForeignKey(Ayat, on_delete=models.CASCADE, related_name='words')
    position = models.PositiveIntegerField()
    arabic = models.CharField(max_length=255)
    transliteration = models.CharField(max_length=255)
    translation_en = models.CharField(max_length=255)
    audio_url = models.URLField(max_length=500, blank=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f"{self.ayat.verse_key} word {self.position}"


class Tafsir(models.Model):
    """Ayat-specific Tafsir (Exegesis)."""
    ayat = models.ForeignKey(Ayat, on_delete=models.CASCADE, related_name='tafsirs')
    source = models.CharField(max_length=255)
    language = models.CharField(max_length=50)
    text = models.TextField()

    def __str__(self):
        return f"Tafsir {self.source} for {self.ayat.verse_key}"


class Reciter(models.Model):
    """Quranic Reciter (Qari) metadata."""
    name = models.CharField(max_length=255)
    style = models.CharField(max_length=255, blank=True)
    audio_url_pattern = models.CharField(max_length=500, help_text="Pattern to construct audio URLs")

    def __str__(self):
        return self.name


class Juz(models.Model):
    """Juz (Para) metadata."""
    number = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255)
    first_surah = models.IntegerField()
    first_ayat = models.IntegerField()
    last_surah = models.IntegerField()
    last_ayat = models.IntegerField()

    class Meta:
        ordering = ['number']
        verbose_name_plural = "Juzs"

    def __str__(self):
        return f"Juz {self.number}"
