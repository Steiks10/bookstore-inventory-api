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
