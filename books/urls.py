from django.urls import path
from .api.views import BookCreateView, BookDetailView

urlpatterns = [
    path('books/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:id>/', BookDetailView.as_view(), name='book-detail'),
]