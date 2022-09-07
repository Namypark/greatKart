from turtle import right
from types import NoneType
from unicodedata import category
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from .models import Product


def search(request):
    search_query = ""
    if request.method == "GET":
        search_query = request.GET.get("search")

        products = (
            Product.objects.distinct()
            .filter(
                Q(product_name__icontains=search_query)
                | Q(slug__icontains=search_query)
            )
            .order_by("created_date")
        )

    return products, search_query


def pagination(request, products):
    page = request.GET.get("page")
    if page == None:
        page = 1
    paginator = Paginator(products, 3)

    try:
        page_obj = paginator.get_page(page)

    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.get_page(page)

    except PageNotAnInteger:
        page = 1
        page_obj = paginator.get_page(page)

    except InvalidPage:
        page = 1
        page_obj = paginator.get_page(page)

    leftIndex = int(page) - 4
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = int(page) + 5
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, page_obj
