from tkinter import N
from django.db import models
import uuid
from accounts.models import Account
from store.models import Product, Variation

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    amount_paid = models.CharField(max_length=200)
    payment_method = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.payment_id)


choices = (
    ("New", "New"),
    ("Accepted", "Accepted"),
    ("Completed", "Completed"),
    ("Cancelled", "Cancelled"),
)


class Order(models.Model):

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=300)
    address_line_1 = models.CharField(max_length=600)
    address_line_2 = models.CharField(max_length=600, blank=True)
    country = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=60)
    tax = models.FloatField()
    ip = models.GenericIPAddressField()
    status = models.CharField(max_length=100, choices=choices, default="New")
    order_total = models.FloatField()
    order_note = models.CharField(max_length=300)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def full_address(self):
        return f"{self.address_line_1}, {self.city}, {self.state},{self.country}"

    def __str__(self) -> str:
        return self.full_name


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
