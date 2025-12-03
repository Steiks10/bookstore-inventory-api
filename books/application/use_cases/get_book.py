from typing import Optional

from ..dto import BookDTO
from ...domain.book import Book
from ...domain.repositories import BookRepository


def _book_to_dto(book: Book) -> BookDTO:
	return BookDTO(
		id=book.id,
		title=book.title,
		author=book.author,
		isbn=book.isbn,
		cost_usd=str(book.cost_usd),
		selling_price_local=str(book.selling_price_local) if book.selling_price_local is not None else None,
		stock_quantity=book.stock_quantity,
		category=book.category,
		supplier_country=book.supplier_country,
		created_at=book.created_at.isoformat(),
		updated_at=book.updated_at.isoformat(),
	)


def get_book_by_id(repository: BookRepository, book_id: int) -> Optional[BookDTO]:
	book = repository.get_by_id(book_id)
	if not book:
		return None
	return _book_to_dto(book)
