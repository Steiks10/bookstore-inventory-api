from django.core.management.base import BaseCommand
from books.domain.book import Book


SAMPLE_BOOKS = [
    {
        "title": "El Quijote",
        "author": "Miguel de Cervantes",
        "isbn": "9788437604947",
        "cost_usd": 15.99,
        "selling_price_local": None,
        "stock_quantity": 25,
        "category": "Literatura Clásica",
        "supplier_country": "ES",
    },
    {
        "title": "Cien años de soledad",
        "author": "Gabriel García Márquez",
        "isbn": "9780307474728",
        "cost_usd": 12.50,
        "selling_price_local": None,
        "stock_quantity": 40,
        "category": "Realismo Mágico",
        "supplier_country": "CO",
    },
    {
        "title": "La ciudad y los perros",
        "author": "Mario Vargas Llosa",
        "isbn": "9788420471839",
        "cost_usd": 10.00,
        "selling_price_local": None,
        "stock_quantity": 18,
        "category": "Novela",
        "supplier_country": "PE",
    },
]


class Command(BaseCommand):
    help = "Seed initial books into the database if not present"

    def handle(self, *args, **options):
        created_count = 0
        for data in SAMPLE_BOOKS:
            isbn = data["isbn"]
            if not Book.objects.filter(isbn=isbn).exists():
                Book.objects.create(**data)
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f"Seed completed. Created {created_count} books."))
