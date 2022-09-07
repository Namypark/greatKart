from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, CartItem
from store.models import Product

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()

    return cart


def add_cart(request, product_id):
    if request.method == "POST":
        color = request.POST.get("color")
        size = request.POST.get("size")
        print(color, size)

    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(
            cart_id=_cart_id(request)
        )  # get the cart using the cart id present in the session,

    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))

    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()

    return redirect("cart")


def remove_cart(request, product_id):
    # 1.) get the cart
    cart = Cart.objects.get(cart_id=_cart_id(request))
    # 2.) get the product by id
    product = get_object_or_404(Product, id=product_id)
    # 3.)get the cart item
    cart_item = CartItem.objects.get(product=product, cart=cart)
    # check if the quantity is grater than 1 if it is
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect("cart")


def delete_cart(request, product_id):

    cart = Cart.objects.get(cart_id=_cart_id(request))
    print(cart)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    cart_item.delete()
    return redirect("cart")


def cart(request, total_price=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total_price += round(cart_item.product.price * cart_item.quantity, 2)
            quantity += cart_item.quantity
        tax = round((total_price * 2) / 100, 2)
        total = round(tax + total_price, 2)
    except CartItem.DoesNotExist:
        pass

    context = {
        "total_price": total_price,
        "total": total,
        "tax": tax,
        "quantity": quantity,
        "cart_items": cart_items,
    }
    return render(request, "carts/cart.html", context)
