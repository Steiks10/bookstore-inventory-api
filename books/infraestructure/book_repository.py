from typing import Dict

from ..domain.book import Book
from ..domain.repositories import BookRepository


class DjangoORMBookRepository(BookRepository):
    def create(self, data: Dict) -> Book:
        return Book.objects.create(
            title=data.get("title"),
            author=data.get("author"),
            isbn=data.get("isbn"),
            cost_usd=data.get("cost_usd"),
            selling_price_local=data.get("selling_price_local"),
            stock_quantity=data.get("stock_quantity"),
            category=data.get("category"),
            supplier_country=data.get("supplier_country"),
        )
    
    def list(self, offset: int | None = None, limit: int | None = None):
        qs = Book.objects.all().order_by('id')
        if offset is not None:
            if limit is not None:
                return list(qs[offset:offset + limit])
            return list(qs[offset:])
        if limit is not None:
            return list(qs[:limit])
        return list(qs)

    def count(self) -> int:
        return Book.objects.count()

    def get_by_id(self, book_id: int) -> Book | None:
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None
