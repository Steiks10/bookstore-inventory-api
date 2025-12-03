from rest_framework import serializers
from ..domain.book import Book

class BookSerializer(serializers.ModelSerializer):
    def validate_cost_usd(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("cost_usd debe ser mayor a 0")
        return value

    def validate_stock_quantity(self, value):
        if value is None or value < 0:
            raise serializers.ValidationError("stock_quantity no puede ser negativo")
        return value

    def validate_isbn(self, value):
        # Permitir guiones/espacios, validar que tenga 10 o 13 dígitos
        cleaned = ''.join(ch for ch in str(value) if ch.isdigit())
        if len(cleaned) not in (10, 13):
            raise serializers.ValidationError("isbn debe tener 10 o 13 dígitos")
        return value

    def validate(self, attrs):
        isbn = attrs.get('isbn')
        if isbn:
            # En update, excluir el propio registro (self.instance) del chequeo de duplicado
            qs = Book.objects.filter(isbn=isbn)
            if self.instance is not None and getattr(self.instance, 'id', None) is not None:
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                raise serializers.ValidationError({'isbn': 'Ya existe un libro con el mismo ISBN'})
        return attrs

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'isbn',
            'cost_usd',
            'selling_price_local',
            'stock_quantity',
            'category',
            'supplier_country',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']