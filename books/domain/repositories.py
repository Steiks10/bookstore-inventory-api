from abc import ABC, abstractmethod
from typing import Dict

from .book import Book


class BookRepository(ABC):
    @abstractmethod
    def create(self, data: Dict) -> Book:
        """Create a book and return the instance."""
        raise NotImplementedError
