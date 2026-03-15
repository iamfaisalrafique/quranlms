from django.contrib import admin
from .models import Surah, Ayat, AyatWord, Tafsir, Reciter, Juz

@admin.register(Surah)
class SurahAdmin(admin.ModelAdmin):
    list_display = ('number', 'name_english', 'name_arabic', 'ayat_count', 'revelation_type')
    search_fields = ('name_english', 'name_arabic', 'number')
    list_filter = ('revelation_type',)

@admin.register(Ayat)
class AyatAdmin(admin.ModelAdmin):
    list_display = ('verse_key', 'surah', 'number', 'juz', 'page')
    search_fields = ('verse_key', 'arabic_text', 'translation_en')
    list_filter = ('surah', 'juz', 'page')

@admin.register(AyatWord)
class AyatWordAdmin(admin.ModelAdmin):
    list_display = ('ayat', 'position', 'arabic', 'translation_en')
    search_fields = ('arabic', 'translation_en')
    list_filter = ('ayat__surah',)

@admin.register(Tafsir)
class TafsirAdmin(admin.ModelAdmin):
    list_display = ('ayat', 'source', 'language')
    list_filter = ('source', 'language')

@admin.register(Reciter)
class ReciterAdmin(admin.ModelAdmin):
    list_display = ('name', 'style')

@admin.register(Juz)
class JuzAdmin(admin.ModelAdmin):
    list_display = ('number', 'name')
