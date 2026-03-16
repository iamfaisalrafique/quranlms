from django.db.models import Q
from rest_framework import generics, status, pagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import HadithCollection, HadithBook, HadithChapter, Hadith
from .serializers import (
    HadithCollectionSerializer, HadithBookSerializer, 
    HadithChapterSerializer, HadithSerializer, HadithSearchSerializer
)
from apps.lessons.models import HadithBookmark

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100

class SearchResultsSetPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50

class CollectionListView(generics.ListAPIView):
    serializer_class = HadithCollectionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        status_filter = self.request.query_params.get('status', 'complete')
        return HadithCollection.objects.filter(status=status_filter).order_by('collection_id')

class CollectionDetailView(generics.RetrieveAPIView):
    queryset = HadithCollection.objects.all()
    serializer_class = HadithCollectionSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['book_count'] = instance.books.count()
        return Response(data)

class BookListView(generics.ListAPIView):
    serializer_class = HadithBookSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        slug = self.kwargs['slug']
        return HadithBook.objects.filter(collection__slug=slug).order_by('book_number')

class ChapterListView(generics.ListAPIView):
    serializer_class = HadithChapterSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        slug = self.kwargs['slug']
        book_number = self.kwargs['book_number']
        return HadithChapter.objects.filter(
            collection__slug=slug,
            book__book_number=book_number
        ).order_by('id')

class HadithListView(generics.ListAPIView):
    serializer_class = HadithSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        slug = self.kwargs['slug']
        book_number = self.kwargs['book_number']
        return Hadith.objects.filter(
            collection__slug=slug,
            book__book_number=book_number
        ).select_related('chapter', 'book', 'collection')

class HadithDetailView(generics.RetrieveAPIView):
    serializer_class = HadithSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        slug = self.kwargs['slug']
        book_number = self.kwargs['book_number']
        hadith_number = self.kwargs['hadith_number']
        return generics.get_object_or_404(
            Hadith,
            collection__slug=slug,
            book__book_number=book_number,
            hadith_number=hadith_number
        )

class SunnahSearchView(generics.ListAPIView):
    serializer_class = HadithSearchSerializer
    permission_classes = [AllowAny]
    pagination_class = SearchResultsSetPagination

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if not query:
            return Hadith.objects.none()
        
        return Hadith.objects.filter(
            Q(english_body__icontains=query) |
            Q(arabic_body__icontains=query) |
            Q(narrator__icontains=query)
        ).select_related('collection', 'book')

class HadithBookmarkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'student_profile'):
            return Response({"detail": "Not a student."}, status=403)
        
        bookmarks = HadithBookmark.objects.filter(student=request.user.student_profile)
        data = [{
            "id": b.id,
            "hadith_id": b.hadith_id,
            "note": b.note,
            "created_at": b.created_at
        } for b in bookmarks]
        return Response(data)

    def post(self, request):
        if not hasattr(request.user, 'student_profile'):
            return Response({"detail": "Not a student."}, status=403)
        
        hadith_id = request.data.get('hadith_id')
        if not hadith_id:
            return Response({"error": "hadith_id is required"}, status=400)

        bookmark, created = HadithBookmark.objects.get_or_create(
            student=request.user.student_profile,
            hadith_id=hadith_id
        )
        
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
