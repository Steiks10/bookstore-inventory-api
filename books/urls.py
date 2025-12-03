from django.urls import path
from .api.views import BooksView, BookView

urlpatterns = [
    path('books/', BooksView.as_view(), name='books'),
    path('books/<int:id>/', BookView.as_view(), name='book'),
]