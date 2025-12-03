from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from .book import Book


class BookRepository(ABC):
    @abstractmethod
    def create(self, data: Dict) -> Book:
        """Create a book and return the instance."""
        raise NotImplementedError

    @abstractmethod
    def list(self, offset: Optional[int] = None, limit: Optional[int] = None) -> List[Book]:
        """Return books with optional pagination (offset/limit)."""
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        """Return total number of books."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Return a book by id or None if not found."""
        raise NotImplementedError

    @abstractmethod
    def update_by_id(self, book_id: int, data: Dict) -> Optional[Book]:
        """Update a book by id with provided data and return instance or None if not found."""
        raise NotImplementedError
