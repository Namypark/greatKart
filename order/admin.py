from django.contrib import admin
from .models import Payment, Order, OrderProduct

# Register your models here.


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ["payment", "user", "product", "quantity", "product_price"]
    extra = 0


class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = [
        "user",
        "payment_method",
        "payment_id",
        "status",
        "amount_paid",
        "date_created",
    ]
    filter = ["date_created"]


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = [
        "full_name",
        "phone",
        "email",
        "city",
        "order_total",
        "tax",
        "payment",
        "status",
        "order_id",
        "created_at",
        "is_ordered",
    ]
    list_filter = ["status", "is_ordered"]
    search_fields = ["order_id", "first_name", "last_name", "phone", "email"]
    inlines = [OrderProductInline]
    list_per_page = 20


class OrderProductAdmin(admin.ModelAdmin):
    model = OrderProduct
    list_display = [
        "user",
        "order",
        "ordered",
        "payment",
        "product",
        "created_at",
        "updated_at",
    ]


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
