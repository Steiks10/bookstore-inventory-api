"""
Simple dependency provider to avoid wiring infra directly in views.
"""

from typing import Protocol

from ..infraestructure.book_repository import DjangoORMBookRepository
from ..domain.repositories import BookRepository


class BookRepositoryProvider(Protocol):
    def get(self) -> BookRepository: ...


class DefaultBookRepositoryProvider:
    def get(self) -> BookRepository:
        return DjangoORMBookRepository()


# Singleton-like default provider that views/use cases can import
book_repository_provider: BookRepositoryProvider = DefaultBookRepositoryProvider()
