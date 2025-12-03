from django.urls import path
from .api.views import BooksView, BookView, BookSearchView, BookLowStockView

urlpatterns = [
    path('books/', BooksView.as_view(), name='books'),
    path('books/<int:id>/', BookView.as_view(), name='book'),
    path('books/search/', BookSearchView.as_view(), name='book-search'),
    path('books/low-stock/', BookLowStockView.as_view(), name='book-low-stock'),
]