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
        fields = '__all__'

class HadithSerializer(serializers.ModelSerializer):
    collection_name = serializers.CharField(source='chapter.book.collection.name_en', read_only=True)
    book_name = serializers.CharField(source='chapter.book.name_en', read_only=True)
    chapter_title = serializers.CharField(source='chapter.title_en', read_only=True)
    
    class Meta:
        model = Hadith
        fields = '__all__'
