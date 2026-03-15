from rest_framework import serializers
from .models import Surah, Ayat, AyatWord, Tafsir, Reciter, Juz

class SurahSerializer(serializers.ModelSerializer):
    class Meta:
        model = Surah
        fields = '__all__'

class AyatWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AyatWord
        fields = '__all__'

class AyatSerializer(serializers.ModelSerializer):
    words = AyatWordSerializer(many=True, read_only=True)
    class Meta:
        model = Ayat
        fields = '__all__'

class TafsirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tafsir
        fields = '__all__'

class ReciterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reciter
        fields = '__all__'

class JuzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Juz
        fields = '__all__'
