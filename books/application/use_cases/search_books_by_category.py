from typing import Optional
from math import ceil

from ..dto import BookDTO, PaginatedBooksDTO
from ...domain.repositories import BookRepository


def _to_dto_items(items):
	return [
		BookDTO(
			id=b.id,
			title=b.title,
			author=b.author,
			isbn=b.isbn,
			cost_usd=str(b.cost_usd),
			selling_price_local=str(b.selling_price_local) if b.selling_price_local is not None else None,
			stock_quantity=b.stock_quantity,
			category=b.category,
			supplier_country=b.supplier_country,
			created_at=b.created_at.isoformat(),
			updated_at=b.updated_at.isoformat(),
		)
		for b in items
	]


def search_books_by_category(repository: BookRepository, category: str, page: Optional[int] = None, page_size: Optional[int] = None) -> PaginatedBooksDTO:
	if not category:
		return PaginatedBooksDTO(items=[], total=0, page=1, page_size=1, total_pages=1)

	if page is not None and page_size is not None:
		page = max(1, int(page))
		page_size = max(1, int(page_size))
		offset = (page - 1) * page_size
		items = repository.search_by_category(category, offset=offset, limit=page_size)
		# Total exact count by filter
		total = len(repository.search_by_category(category))
		total_pages = max(1, ceil(total / page_size)) if total else 1
		return PaginatedBooksDTO(items=_to_dto_items(items), total=total, page=page, page_size=page_size, total_pages=total_pages)

	items = repository.search_by_category(category)
	total = len(items)
	return PaginatedBooksDTO(items=_to_dto_items(items), total=total, page=1, page_size=total or 1, total_pages=1)

