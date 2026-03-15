from django.urls import path
from . import views

urlpatterns = [
    path('collections/', views.CollectionListView.as_view(), name='collection-list'),
    path('collection/<slug:slug>/books/', views.BookListView.as_view(), name='book-list'),
    path('collection/<slug:slug>/book/<str:num>/chapters/', views.ChapterListView.as_view(), name='chapter-list'),
    path('collection/<slug:slug>/book/<str:num>/hadiths/', views.HadithListView.as_view(), name='hadith-list'),
    path('hadith/<int:pk>/', views.HadithDetailView.as_view(), name='hadith-detail'),
    path('search/', views.SunnahSearchView.as_view(), name='sunnah-search'),
    
    # Bookmarks
    path('bookmarks/', views.HadithBookmarkView.as_view(), name='hadith-bookmark-list'),
    path('bookmark/', views.HadithBookmarkView.as_view(), name='hadith-bookmark-create'),
    path('bookmark/<int:pk>/', views.HadithBookmarkDeleteView.as_view(), name='hadith-bookmark-delete'),
]
