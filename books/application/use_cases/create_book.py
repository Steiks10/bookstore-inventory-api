from typing import Dict
from ...domain.book import Book
from ...domain.repositories import BookRepository


def create_book(data: Dict, repository: BookRepository) -> Book:
	"""Use case for creating a book via repository abstraction."""
	return repository.create(data)
