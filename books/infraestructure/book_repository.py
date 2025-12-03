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

    def update_by_id(self, book_id: int, data: Dict) -> Book | None:
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None

        for field in [
            "title",
            "author",
            "isbn",
            "cost_usd",
            "selling_price_local",
            "stock_quantity",
            "category",
            "supplier_country",
        ]:
            if field in data:
                setattr(book, field, data[field])

        book.save()
        return book

    def delete_by_id(self, book_id: int) -> bool:
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return False
        book.delete()
        return True

    def search_by_category(self, category: str, offset: int | None = None, limit: int | None = None):
        qs = Book.objects.filter(category__icontains=category).order_by('id')
        if offset is not None:
            if limit is not None:
                return list(qs[offset:offset + limit])
            return list(qs[offset:])
        if limit is not None:
            return list(qs[:limit])
        return list(qs)

    def list_low_stock(self, threshold: int, offset: int | None = None, limit: int | None = None):
        qs = Book.objects.filter(stock_quantity__lt=threshold).order_by('id')
        if offset is not None:
            if limit is not None:
                return list(qs[offset:offset + limit])
            return list(qs[offset:])
        if limit is not None:
            return list(qs[:limit])
        return list(qs)
