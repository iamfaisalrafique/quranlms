from django.urls import path
from . import views

urlpatterns = [
    path('surahs/', views.SurahListView.as_view(), name='surah-list'),
    path('surah/<int:number>/', views.SurahDetailView.as_view(), name='surah-detail'),
    path('surah/<int:number>/ayat/', views.SurahAyatListView.as_view(), name='surah-ayat-list'),
    path('ayat/<int:pk>/words/', views.AyatWordListView.as_view(), name='ayat-word-list'),
    path('ayat/<int:pk>/tafsir/', views.AyatTafsirListView.as_view(), name='ayat-tafsir-list'),
    path('juz/<int:number>/', views.JuzDetailView.as_view(), name='juz-detail'),
    path('page/<int:number>/', views.PageDetailView.as_view(), name='page-detail'),
    path('search/', views.QuranSearchView.as_view(), name='quran-search'),
    path('reciters/', views.ReciterListView.as_view(), name='reciter-list'),
    
    # Bookmarks
    path('bookmarks/', views.QuranBookmarkView.as_view(), name='bookmark-list'),
    path('bookmark/', views.QuranBookmarkView.as_view(), name='bookmark-create'),
    path('bookmark/<int:pk>/', views.QuranBookmarkDeleteView.as_view(), name='bookmark-delete'),
]
