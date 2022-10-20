from django.contrib import admin

from .models import Product, ProductsGallery, ReviewRating, Variation
import admin_thumbnails
# Register your models here.


@admin_thumbnails.thumbnail("image")
class ProductGalleryInline(admin.TabularInline):
    model = ProductsGallery
    extra = 1


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
    inlines = [ProductGalleryInline]


class VariationAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "variation_category",
        "variation_value",
        "is_active",
        "created_date",
    )
    list_editable = ("is_active",)
    list_filter = ["product", "variation_category", "variation_value", "is_active"]


admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductsGallery)
