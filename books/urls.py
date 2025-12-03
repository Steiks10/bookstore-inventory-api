from django.urls import path
from .api.views import BooksView, BookView, BookSearchView, BookLowStockView, BookCalculatePriceView

urlpatterns = [
    # Lista libros y crea nuevos
    path('books/', BooksView.as_view(), name='books'),
    # Obtiene/actualiza/elimina un libro por ID
    path('books/<int:id>/', BookView.as_view(), name='book'),
    # Calcula precio sugerido para un libro
    path('books/<int:id>/calculate-price/', BookCalculatePriceView.as_view(), name='book-calculate-price'),
    # Busca libros por categoría
    path('books/search/', BookSearchView.as_view(), name='book-search'),
    # Lista libros con stock bajo
    path('books/low-stock/', BookLowStockView.as_view(), name='book-low-stock'),
]