from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError, DatabaseError

from .serializers import BookSerializer
from ..application.use_cases.create_book import create_book
from ..controllers.container import book_repository_provider


class BookCreateView(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            repo = book_repository_provider.get()
            book = create_book(serializer.validated_data, repo)
            output = BookSerializer(book)
            return Response(output.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            # Likely duplicate ISBN constraint or similar
            return Response({"detail": "Datos inválidos o duplicados", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as e:
            # Database down or connection issues → treat as service unavailable
            return Response({"detail": "Servicio de base de datos no disponible", "error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            # Unexpected server error
            return Response({"detail": "Error interno del servidor", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
