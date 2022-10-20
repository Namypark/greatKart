from tkinter import PhotoImage
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import UserProfile
from carts.models import CartItem
from category.models import Category
from order.models import OrderProduct
from store.forms import ReviewForm
from .models import Product, ProductsGallery, ReviewRating
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
    if request.user.is_authenticated:
        try:
            order_product = OrderProduct.objects.filter(
                user=request.user, product_id=single_product.id
            ).exists()

        except OrderProduct.DoesNotExist:
            order_product = None
    else:
        order_product = None
    # GET reviews
    reviews = ReviewRating.objects.filter(
        product_id=single_product.id, status=True
    ).order_by("created_at")
    
    #get other images from product gallery
    products_gallery = ProductsGallery.objects.filter(product_id=single_product.id)
    context = {
        "single_product": single_product,
        "in_cart": in_cart,
        "range": range(10, 0, -1),
        "order_product": order_product,
        "reviews": reviews,
        "products_gallery": products_gallery,
    }

    return render(request, "store/product-detail.html", context)


def review(request, product_id):
    url = request.META.get("HTTP_REFERER")
    product = Product.objects.get(id=product_id)

    if request.method == "POST":

        try:

            review_rating = ReviewRating.objects.get(
                user__id=request.user.id, product=product
            )
            form = ReviewForm(request.POST, instance=review_rating)
            form.save()
            messages.success(request, "Thank you your review has been updated")
            return redirect(url)
        except ReviewRating.DoesNotExist:

            form = ReviewForm(request.POST)
            print(form.is_valid())
            if form.is_valid():
                print(form.data)
                data = ReviewRating()
                data.product_id = product_id
                data.user = request.user
                data.review = form.cleaned_data["review"]
                data.subject = form.cleaned_data["subject"]
                data.rating = form.cleaned_data["rating"]
                data.ip = request.META.get("REMOTE_ADDR")
                data.save()
                messages.success(request, "Thank you your review has been updated")
                return redirect(url)
