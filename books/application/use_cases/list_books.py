from dataclasses import asdict
from math import ceil
from typing import Optional, Tuple

from ..dto import BookDTO, PaginatedBooksDTO
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


def list_books(repository: BookRepository, page: Optional[int] = None, page_size: Optional[int] = None) -> PaginatedBooksDTO:
	if page is not None and page_size is not None:
		page = max(1, int(page))
		page_size = max(1, int(page_size))
		offset = (page - 1) * page_size
		items = repository.list(offset=offset, limit=page_size)
		total = repository.count()
		total_pages = max(1, ceil(total / page_size)) if total else 1
		dto_items = [_book_to_dto(b) for b in items]
		return PaginatedBooksDTO(items=dto_items, total=total, page=page, page_size=page_size, total_pages=total_pages)

	# No pagination requested: return all
	items = repository.list()
	total = len(items)
	dto_items = [_book_to_dto(b) for b in items]
	# Normalize to a single-page response
	return PaginatedBooksDTO(items=dto_items, total=total, page=1, page_size=total or 1, total_pages=1)

