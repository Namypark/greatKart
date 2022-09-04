from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Product


def pagination(request):
    store_products = (
        Product.objects.all()
    )  # fetching all product objects from the database
    paginator = Paginator(
        store_products, 3
    )  # creating a paginator object, with the number of pages to create
    # shows 3 products per page

    page_number = request.GET.get("page")  # returns the desired number from URL
    try:

        page_obj = Paginator.get_page(page_number)
        # returns the desired page object
    except PageNotAnInteger:
        page_obj = paginator.page(1)
        # returns the first page if page is not an integer
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
        # returns the last page if page is empty

    context = {"page_obj": page_obj}

    return render(request, "store/store.html", context)
