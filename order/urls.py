from django.urls import path
from . import views


urlpatterns = [
    path("place-order/", views.place_order, name="place_order"),
    path("payment/", views.payments, name="payments"),
    path("payment/order_complete/", views.order_complete, name="order_complete"),
]
