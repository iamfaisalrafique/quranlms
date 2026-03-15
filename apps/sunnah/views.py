from django.db.models import Q
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import HadithCollection, HadithBook, HadithChapter, Hadith
from .serializers import (
    HadithCollectionSerializer, HadithBookSerializer, 
    HadithChapterSerializer, HadithSerializer
)
from apps.lessons.models import HadithBookmark

class CollectionListView(generics.ListAPIView):
    queryset = HadithCollection.objects.all()
    serializer_class = HadithCollectionSerializer
    permission_classes = [AllowAny]

class BookListView(generics.ListAPIView):
    serializer_class = HadithBookSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        collection_slug = self.kwargs['slug']
        return HadithBook.objects.filter(collection__slug=collection_slug)

class ChapterListView(generics.ListAPIView):
    serializer_class = HadithChapterSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        collection_slug = self.kwargs['slug']
        book_num = self.kwargs['num']
        return HadithChapter.objects.filter(
            book__collection__slug=collection_slug,
            book__book_number=book_num
        )

class HadithListView(generics.ListAPIView):
    serializer_class = HadithSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        collection_slug = self.kwargs['slug']
        book_num = self.kwargs['num']
        return Hadith.objects.filter(
            chapter__book__collection__slug=collection_slug,
            chapter__book__book_number=book_num
        ).select_related('chapter__book__collection')

class HadithDetailView(generics.RetrieveAPIView):
    queryset = Hadith.objects.all()
    serializer_class = HadithSerializer
    permission_classes = [AllowAny]

class SunnahSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"results": []})
        
        results = Hadith.objects.filter(
            Q(text_en__icontains=query) | 
            Q(text_ur__icontains=query) |
            Q(arabic_text__icontains=query) |
            Q(narrator_en__icontains=query)
        )[:50]
        
        serializer = HadithSerializer(results, many=True)
        return Response({"results": serializer.data})

# ── Bookmark Views ────────────────────────────────────────────────────────────

class HadithBookmarkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'student_profile'):
            return Response({"detail": "Not a student."}, status=403)
        
        bookmarks = HadithBookmark.objects.filter(student=request.user.student_profile)
        data = [{
            "id": b.id,
            "hadith_id": b.hadith_id,
            "urn": b.hadith.urn,
            "note": b.note,
            "created_at": b.created_at
        } for b in bookmarks]
        return Response(data)

    def post(self, request):
        if not hasattr(request.user, 'student_profile'):
            return Response({"detail": "Not a student."}, status=403)
        
        hadith_id = request.data.get('hadith_id')
        note = request.data.get('note', '')
        
        bookmark, created = HadithBookmark.objects.get_or_create(
            student=request.user.student_profile,
            hadith_id=hadith_id,
            defaults={'note': note}
        )
        
        if not created:
            bookmark.note = note
            bookmark.save()
            
        return Response({"id": bookmark.id, "created": created}, status=status.HTTP_201_CREATED)

class HadithBookmarkDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        if not hasattr(request.user, 'student_profile'):
            return Response({"detail": "Not a student."}, status=403)
            
        HadithBookmark.objects.filter(
            id=pk, student=request.user.student_profile
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
