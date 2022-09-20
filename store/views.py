from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from carts.models import CartItem
from category.models import Category
from .models import Product
from carts.views import _cart_id
from .utils import search, pagination

# Create your views here.


def search_store(request):
    products, search_query = search(request)

    custom_range, page_obj = pagination(request, products)

    product_count = products.count()

    context = {
        "products": page_obj,
        "product_count": product_count,
        "search_query": search_query,
        "custom_range": custom_range,
    }
    return render(request, "store/store.html", context)


def store(request, category_slug=None):

    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True
        ).order_by("id")
        custom_range, page_obj = pagination(request, products)

        product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True).order_by("id")

        custom_range, page_obj = pagination(request, products)

        product_count = products.count()

    context = {
        "products": page_obj,
        "product_count": product_count,
        "categories": categories,
        "custom_range": custom_range,
    }

    return render(request, "store/store.html", context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug
        )
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), product=single_product
        ).exists()

    except Exception as e:
        raise e
    context = {"single_product": single_product, "in_cart": in_cart}

    return render(request, "store/product-detail.html", context)
