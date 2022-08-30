from carts.models import CartItem
from django.db.models import Sum


def cart_quantity(request):
    if "admin" in request.path:
        return {}

    else:
        quantity = CartItem.objects.all().aggregate(Sum("quantity"))
        return dict(quantity=quantity["quantity__sum"])
