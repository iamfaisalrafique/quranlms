from django.contrib import admin
from .models import HadithCollection, HadithBook, HadithChapter, Hadith

@admin.register(HadithCollection)
class HadithCollectionAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name_en', 'name_ar', 'total_hadiths')
    search_fields = ('slug', 'name_en', 'name_ar')

@admin.register(HadithBook)
class HadithBookAdmin(admin.ModelAdmin):
    list_display = ('collection', 'book_number', 'name_en')
    list_filter = ('collection',)
    search_fields = ('name_en', 'book_number')

@admin.register(HadithChapter)
class HadithChapterAdmin(admin.ModelAdmin):
    list_display = ('book', 'chapter_number', 'title_en')
    list_filter = ('book__collection', 'book')
    search_fields = ('title_en', 'chapter_number')

@admin.register(Hadith)
class HadithAdmin(admin.ModelAdmin):
    list_display = ('hadith_number', 'chapter', 'grade', 'urn')
    list_filter = ('chapter__book__collection', 'grade')
    search_fields = ('arabic_text', 'text_en', 'hadith_number', 'urn')
