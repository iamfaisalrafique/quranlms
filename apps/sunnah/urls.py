from django.urls import path
from . import views

urlpatterns = [
    path('collections/', views.CollectionListView.as_view(), name='collection-list'),
    path('search/', views.SunnahSearchView.as_view(), name='sunnah-search'),
    path('bookmarks/', views.HadithBookmarkView.as_view(), name='hadith-bookmark-list'),
    path('bookmark/', views.HadithBookmarkView.as_view(), name='hadith-bookmark-create'),
    path('bookmark/<int:pk>/', views.HadithBookmarkDeleteView.as_view(), name='hadith-bookmark-delete'),  
    path('<slug:slug>/', views.CollectionDetailView.as_view(), name='collection-detail'),
    path('<slug:slug>/books/', views.BookListView.as_view(), name='book-list'),
    path('<slug:slug>/books/<str:book_number>/chapters/', views.ChapterListView.as_view(), name='chapter-list'),
    path('<slug:slug>/<str:book_number>/hadiths/', views.HadithListView.as_view(), name='hadith-list'),   
    path('<slug:slug>/<str:book_number>/<str:hadith_number>/', views.HadithDetailView.as_view(), name='hadith-detail'),
]
