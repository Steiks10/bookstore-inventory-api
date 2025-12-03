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
from ..application.use_cases.get_book import get_book_by_id
from ..application.use_cases.update_book import update_book_by_id
from ..application.use_cases.delete_book import delete_book_by_id
from ..application.use_cases.search_books_by_category import search_books_by_category
from ..controllers.container import book_repository_provider


class BooksView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(name='page', description='Número de página (>=1)', required=False, type=int),
            OpenApiParameter(name='page_size', description='Tamaño de página (>=1)', required=False, type=int),
        ],
        responses={200: BookSerializer(many=True)},
    )
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
        
    @extend_schema(
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


class BookView(APIView):
    def get(self, request, id: int):
        try:
            repo = book_repository_provider.get()
            dto = get_book_by_id(repo, id)
            if dto is None:
                return Response({"detail": "Libro no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            data = {
                'id': dto.id,
                'title': dto.title,
                'author': dto.author,
                'isbn': dto.isbn,
                'cost_usd': dto.cost_usd,
                'selling_price_local': dto.selling_price_local,
                'stock_quantity': dto.stock_quantity,
                'category': dto.category,
                'supplier_country': dto.supplier_country,
                'created_at': dto.created_at,
                'updated_at': dto.updated_at,
            }
            return Response(data, status=status.HTTP_200_OK)
        except DatabaseError as e:
            return Response({"detail": "Servicio de base de datos no disponible", "error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({"detail": "Error interno del servidor", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        request=BookSerializer,
        responses={200: BookSerializer},
        examples=[
            OpenApiExample(
                'Ejemplo de actualización de libro',
                value={
                    "title": "El Quijote (Edición Revisada)",
                    "author": "Miguel de Cervantes",
                    "isbn": "978-84-376-0494-7",
                    "cost_usd": "17.99",
                    "selling_price_local": None,
                    "stock_quantity": 30,
                    "category": "Literatura Clásica",
                    "supplier_country": "ES"
                },
                request_only=True,
            ),
        ],
    )
    def put(self, request, id: int):
        try:
            repo = book_repository_provider.get()
            # Ensure the book exists
            existing = repo.get_by_id(id)
            if existing is None:
                return Response({"detail": "Libro no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            # Validate full update via serializer using existing instance
            serializer = BookSerializer(instance=existing, data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Prevent duplicate ISBN (exclude current id)
            isbn = serializer.validated_data.get("isbn")
            if isbn is not None:
                from ..domain.book import Book as BookModel
                if BookModel.objects.filter(isbn=isbn).exclude(id=id).exists():
                    return Response({"isbn": ["Ya existe un libro con el mismo ISBN"]}, status=status.HTTP_400_BAD_REQUEST)

            dto = update_book_by_id(repo, id, serializer.validated_data)
            if dto is None:
                return Response({"detail": "Libro no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            data = {
                'id': dto.id,
                'title': dto.title,
                'author': dto.author,
                'isbn': dto.isbn,
                'cost_usd': dto.cost_usd,
                'selling_price_local': dto.selling_price_local,
                'stock_quantity': dto.stock_quantity,
                'category': dto.category,
                'supplier_country': dto.supplier_country,
                'created_at': dto.created_at,
                'updated_at': dto.updated_at,
            }
            return Response(data, status=status.HTTP_200_OK)
        except IntegrityError as e:
            return Response({"detail": "Datos inválidos o duplicados", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as e:
            return Response({"detail": "Servicio de base de datos no disponible", "error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({"detail": "Error interno del servidor", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, id: int):
        try:
            repo = book_repository_provider.get()
            deleted = delete_book_by_id(repo, id)
            if not deleted:
                return Response({"detail": "Libro no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except DatabaseError as e:
            return Response({"detail": "Servicio de base de datos no disponible", "error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({"detail": "Error interno del servidor", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


class BookSearchView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(name='category', description='Categoría a buscar', required=True, type=str),
            OpenApiParameter(name='page', description='Número de página (>=1)', required=False, type=int),
            OpenApiParameter(name='page_size', description='Tamaño de página (>=1)', required=False, type=int),
        ],
        responses={200: BookSerializer(many=True)},
    )
    def get(self, request):
        try:
            category = request.query_params.get('category')
            if category is None or category.strip() == '':
                return Response({'detail': 'category es requerido'}, status=status.HTTP_400_BAD_REQUEST)
            page = request.query_params.get('page')
            page_size = request.query_params.get('page_size')
            page = int(page) if page is not None else None
            page_size = int(page_size) if page_size is not None else None
            repo = book_repository_provider.get()
            dto = search_books_by_category(repository=repo, category=category, page=page, page_size=page_size)
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

    
