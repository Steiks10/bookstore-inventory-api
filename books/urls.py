from django.urls import path
from .api.views import BookCreateView

urlpatterns = [
    path('books/', BookCreateView.as_view(), name='book-create'),
]