from ...domain.repositories import BookRepository


def delete_book_by_id(repository: BookRepository, book_id: int) -> bool:
	return repository.delete_by_id(book_id)

