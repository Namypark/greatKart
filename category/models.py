import uuid
from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):

    name = models.CharField(max_length=50)
    slug = models.SlugField(null=True)
    description = models.TextField(max_length=200, blank=True)
    image = models.ImageField(blank=True, null=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    # WE USE THE GET ABSOLUTE URL TO GET CANONICAL URL PATTERNS
    def get_absolute_url(self):
        return reverse("products_by_category", kwargs={"category_slug": self.slug})

    def __str__(self):
        return self.name
