from django.db.models import Q
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Surah, Ayat, AyatWord, Tafsir, Reciter, Juz
from .serializers import (
    SurahSerializer, AyatSerializer, AyatWordSerializer, 
    TafsirSerializer, ReciterSerializer, JuzSerializer
)
from apps.lessons.models import QuranBookmark

class SurahListView(generics.ListAPIView):
    queryset = Surah.objects.all()
    serializer_class = SurahSerializer
    permission_classes = [AllowAny]

class SurahDetailView(generics.RetrieveAPIView):
    queryset = Surah.objects.all()
    serializer_class = SurahSerializer
    lookup_field = 'number'
    permission_classes = [AllowAny]

class SurahAyatListView(generics.ListAPIView):
    serializer_class = AyatSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        surah_number = self.kwargs['number']
        return Ayat.objects.filter(surah__number=surah_number).prefetch_related('words')

class AyatWordListView(generics.ListAPIView):
    serializer_class = AyatWordSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        ayat_id = self.kwargs['pk']
        return AyatWord.objects.filter(ayat_id=ayat_id)

class AyatTafsirListView(generics.ListAPIView):
    serializer_class = TafsirSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        ayat_id = self.kwargs['pk']
        # Defaulting to Mustafa Khattab or first available
        return Tafsir.objects.filter(ayat_id=ayat_id)

class JuzDetailView(generics.ListAPIView):
    serializer_class = AyatSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        juz_number = self.kwargs['number']
        return Ayat.objects.filter(juz=juz_number).prefetch_related('words')

class PageDetailView(generics.ListAPIView):
    serializer_class = AyatSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        page_number = self.kwargs['number']
        return Ayat.objects.filter(page=page_number).prefetch_related('words')

class QuranSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"results": []})
        
        results = Ayat.objects.filter(
            Q(translation_en__icontains=query) | 
            Q(translation_ur__icontains=query) |
            Q(arabic_text__icontains=query)
        )[:50]
        
        serializer = AyatSerializer(results, many=True)
        return Response({"results": serializer.data})

class ReciterListView(generics.ListAPIView):
    queryset = Reciter.objects.all()
    serializer_class = ReciterSerializer
    permission_classes = [AllowAny]

# ── Bookmark Views ────────────────────────────────────────────────────────────

class QuranBookmarkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'student_profile'):
            return Response({"detail": "Not a student."}, status=403)
        
        bookmarks = QuranBookmark.objects.filter(student=request.user.student_profile)
        # We can create a simple serializer here or return raw data
        data = [{
            "id": b.id,
            "ayat_id": b.ayat_id,
            "verse_key": b.ayat.verse_key,
            "note": b.note,
            "created_at": b.created_at
        } for b in bookmarks]
        return Response(data)

    def post(self, request):
        if not hasattr(request.user, 'student_profile'):
            return Response({"detail": "Not a student."}, status=403)
        
        ayat_id = request.data.get('ayat_id')
        note = request.data.get('note', '')
        
        bookmark, created = QuranBookmark.objects.get_or_create(
            student=request.user.student_profile,
            ayat_id=ayat_id,
            defaults={'note': note}
        )
        
        if not created:
            bookmark.note = note
            bookmark.save()
            
        return Response({"id": bookmark.id, "created": created}, status=status.HTTP_201_CREATED)

class QuranBookmarkDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        if not hasattr(request.user, 'student_profile'):
            return Response({"detail": "Not a student."}, status=403)
            
        QuranBookmark.objects.filter(
            id=pk, student=request.user.student_profile
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
