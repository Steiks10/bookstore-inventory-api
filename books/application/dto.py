from dataclasses import dataclass
from typing import List, Optional


@dataclass
class BookDTO:
	id: int
	title: str
	author: str
	isbn: str
	cost_usd: str
	selling_price_local: Optional[str]
	stock_quantity: int
	category: str
	supplier_country: str
	created_at: str
	updated_at: str


@dataclass
class PaginatedBooksDTO:
	items: List[BookDTO]
	total: int
	page: int
	page_size: int
	total_pages: int

