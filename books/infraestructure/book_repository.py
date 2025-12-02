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
