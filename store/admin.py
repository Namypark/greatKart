import site
from django.contrib import admin

from .models import Product

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    prepopulated_fields = {"slug": ("product_name",)}
    list_display = (
        "product_name",
        "price",
        "stock",
        "category",
        "modified_date",
        "is_available",
    )
