from .models import Cart, CartItem
from .views import _cart_id
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum


def cart_quantity(request):
    quantity = 0

    if "admin" in request.path:
        return {}

    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)

            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for item in cart_items:
                quantity += item.quantity

        except Cart.DoesNotExist:
            quantity = 0

    return {"quantity": quantity}


# from .models import Cart, CartItem
# from django.core.exceptions import ObjectDoesNotExist
# from .views import _cart_id


# def cart_quantity(request):
#     cart = Cart.objects.get(cart_id=_cart_id(request))
#     quantity = 0
#     if "admin" in request.path:
#         return {}

#     else:
#         try:
#             # cart = Cart.objects.get(cart_id=_cart_id(request))
#             if request.user.is_authenticated:
#                 cart_item = CartItem.objects.all().filter(user=request.user)

#             else:
#                 cart_item = CartItem.objects.all().filter(cart=cart[:1])

#             for item in cart_item:
#                 quantity += item.quantity
#         except cart.DoesNotExist:
#             quantity = 0
#     return dict(quantity=quantity)
