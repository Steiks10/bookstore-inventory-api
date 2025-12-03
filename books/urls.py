from django.urls import path
from .api.views import BooksView, BookView, BookSearchView

urlpatterns = [
    path('books/', BooksView.as_view(), name='books'),
    path('books/<int:id>/', BookView.as_view(), name='book'),
    path('books/search/', BookSearchView.as_view(), name='book-search'),
]