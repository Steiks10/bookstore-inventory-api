from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
try:
    from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
except Exception:  # graceful fallback if not installed in editor
    def extend_schema(*args, **kwargs):
        def _decorator(cls):
            return cls
        return _decorator
    class OpenApiParameter:  # type: ignore
        def __init__(self, *args, **kwargs):
            pass
from django.db import IntegrityError, DatabaseError

from .serializers import BookSerializer
from ..application.use_cases.create_book import create_book
from ..application.use_cases.list_books import list_books
from ..controllers.container import book_repository_provider


@extend_schema(
    parameters=[
        OpenApiParameter(name='page', description='Número de página (>=1)', required=False, type=int),
        OpenApiParameter(name='page_size', description='Tamaño de página (>=1)', required=False, type=int),
    ],
    request=BookSerializer,
    responses={201: BookSerializer},
    examples=[
        OpenApiExample(
            'Ejemplo de creación de libro',
            value={
                "title": "El Quijote",
                "author": "Miguel de Cervantes",
                "isbn": "978-84-376-0494-7",
                "cost_usd": "15.99",
                "selling_price_local": None,
                "stock_quantity": 25,
                "category": "Literatura Clásica",
                "supplier_country": "ES"
            },
            request_only=True,
        ),
    ],
)
class BookCreateView(APIView):
    def get(self, request):
        try:
            page = request.query_params.get('page')
            page_size = request.query_params.get('page_size')
            page = int(page) if page is not None else None
            page_size = int(page_size) if page_size is not None else None
            repo = book_repository_provider.get()
            dto = list_books(repository=repo, page=page, page_size=page_size)
            # manual dict serialization to avoid importing asdict in the view
            data = {
                'items': [
                    {
                        'id': book.id,
                        'title': book.title,
                        'author': book.author,
                        'isbn': book.isbn,
                        'cost_usd': book.cost_usd,
                        'selling_price_local': book.selling_price_local,
                        'stock_quantity': book.stock_quantity,
                        'category': book.category,
                        'supplier_country': book.supplier_country,
                        'created_at': book.created_at,
                        'updated_at': book.updated_at,
                    } for book in dto.items
                ],
                'total': dto.total,
                'page': dto.page,
                'page_size': dto.page_size,
                'total_pages': dto.total_pages,
            }
            return Response(data, status=status.HTTP_200_OK)
        except ValueError:
            return Response({'detail': 'page y page_size deben ser enteros positivos'}, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as e:
            return Response({"detail": "Servicio de base de datos no disponible", "error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({"detail": "Error interno del servidor", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
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
