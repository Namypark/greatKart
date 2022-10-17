from django.urls import path
from . import views


urlpatterns = [
    path("", views.store, name="store"),
    path("search/", views.search_store, name="search_store"),
    path("category/<slug:category_slug>/", views.store, name="products_by_category"),
    path(
        "category/<slug:category_slug>/<slug:product_slug>/",
        views.product_detail,
        name="product_detail",
    ),
    path("submit_review/<int:product_id>/", views.review, name="review"),
]
