from rest_framework import serializers
from .models import HadithCollection, HadithBook, HadithChapter, Hadith

class HadithCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HadithCollection
        fields = '__all__'

class HadithBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = HadithBook
        fields = '__all__'

class HadithChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HadithChapter
        fields = ['chapter_number', 'english_title', 'arabic_title']

class HadithSerializer(serializers.ModelSerializer):
    book_number = serializers.ReadOnlyField(source='book.book_number')
    chapter = HadithChapterSerializer(read_only=True)

    class Meta:
        model = Hadith
        fields = [
            'id', 'hadith_number', 'arabic_body', 'english_body',
            'narrator', 'grade', 'reference', 'book_number', 'chapter'
        ]

class HadithSearchSerializer(serializers.ModelSerializer):
    collection_slug = serializers.ReadOnlyField(source='collection.slug')
    collection_name = serializers.ReadOnlyField(source='collection.english_title')
    book_number = serializers.ReadOnlyField(source='book.book_number')

    class Meta:
        model = Hadith
        fields = [
            'id', 'hadith_number', 'arabic_body', 'english_body',
            'narrator', 'grade', 'reference', 'collection_slug', 
            'collection_name', 'book_number'
        ]
