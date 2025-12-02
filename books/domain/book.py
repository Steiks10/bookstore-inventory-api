from django.db import models

class Book(models.Model):
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	isbn = models.CharField(max_length=20)
	cost_usd = models.DecimalField(max_digits=10, decimal_places=2)
	selling_price_local = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	stock_quantity = models.IntegerField()
	category = models.CharField(max_length=100)
	supplier_country = models.CharField(max_length=2)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.title} by {self.author}"

	class Meta:
		db_table = "books"
  