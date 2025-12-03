"""
Simple dependency provider to avoid wiring infra directly in views.
"""

from typing import Protocol

from ..infraestructure.book_repository import DjangoORMBookRepository
from ..infraestructure.rates_provider import HttpRatesProvider
from ..domain.repositories import BookRepository
from ..domain.rates import RatesProvider


class BookRepositoryProvider(Protocol):
    def get(self) -> BookRepository: ...


class DefaultBookRepositoryProvider:
    def get(self) -> BookRepository:
        return DjangoORMBookRepository()


# Singleton-like default provider that views/use cases can import
book_repository_provider: BookRepositoryProvider = DefaultBookRepositoryProvider()


class RatesProviderProvider(Protocol):
    def get(self) -> RatesProvider: ...


class DefaultRatesProviderProvider:
    def get(self) -> RatesProvider:
        return HttpRatesProvider()


rates_provider_provider: RatesProviderProvider = DefaultRatesProviderProvider()
