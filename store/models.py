from email.policy import default
from itertools import product
from tabnanny import verbose
from django.db import models
from django.db.models import Avg, Count
from django.urls import reverse
import uuid
from accounts.models import Account
from category.models import Category


# Create your models here.
class Product(models.Model):

    product_name = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to="photos/products")
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse(
            "product_detail",
            kwargs={"product_slug": self.slug, "category_slug": self.category.slug},
        )

    def __str__(self):
        return self.product_name

    def average_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(
            average=Avg("rating")
        )
        avg = 0
        if reviews["average"] != None:
            avg = float(reviews["average"])
        return avg

    def counter_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(
            count=Count("id")
        )
        count = 0
        if reviews["count"] != None:
            count = int(reviews["count"])
        return count


choices = (("color", "color"), ("size", "size"))


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(
            variation_category="color", is_active=True
        )

    def sizes(self):
        return super(VariationManager, self).filter(
            variation_category="size", is_active=True
        )


class Variation(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=choices)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=150, blank=True)
    review = models.TextField(max_length=1000, blank=True)
    rating = models.FloatField()
    ip = models.GenericIPAddressField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class ProductsGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to="store/products", max_length=250)

    class Meta:
        verbose_name = "productgallery"
        verbose_name_plural = "product gallery"

    def _str__(self):
        return self.product.product_name
