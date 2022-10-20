from django.shortcuts import render
from store.models import Product, ReviewRating

# Create your views here.


def index(request):
    products = Product.objects.filter(is_available=True).order_by("created_date")
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
    context = {"products": products, "reviews": reviews}
    return render(request, "ecommerce/index.html", context)
