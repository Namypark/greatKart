from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, CartItem
from store.models import Product, Variation

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()

    return cart


def add_cart(request, product_id):
    # getting the product here
    product = Product.objects.get(id=product_id)
    # getting the product variation here
    product_variation = []
    variation = ""
    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST.get(key)
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value,
                )
                product_variation.append(variation)

            except:
                pass

    # GETTING THE CART HERE
    try:
        cart = Cart.objects.get(
            cart_id=_cart_id(request)
        )  # get the cart using the cart id present in the session,

    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))

    cart.save()
    # GETTING THE CART ITEM HERE
    is_cart_item_exist = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exist:
        cart_item = CartItem.objects.filter(product=product, cart=cart)

        # existing variations --> Database
        # current variations --> product_variation
        # item id --> database

        existing_variation_list = []
        id = []
        for item in cart_item:
            existing_variations = item.variations.all()
            existing_variation_list.append(list(existing_variations))
            id.append(item.id)
        print(existing_variations)
        if product_variation in existing_variation_list:
            # increase the cartItem quantity
            index = existing_variation_list.index(product_variation)
            print(index)
            item_id = id[index]
            print(item_id)
            item = CartItem.objects.get(product=product, id=item_id)
            print(item)
            item.quantity += 1
            item.save()
        else:
            # create a new item
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)

        if len(product_variation) > 0:
            cart_item.variations.clear()

            cart_item.variations.add(*product_variation)

        cart_item.save()

    return redirect("cart")


def remove_cart(request, product_id, cart_item_id):
    # 1.) get the cart
    cart = Cart.objects.get(cart_id=_cart_id(request))
    # 2.) get the product by id
    product = get_object_or_404(Product, id=product_id)
    try:
        # 3.)get the cart item
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        # check if the quantity is grater than 1 if it is
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect("cart")


def delete_cart(request, product_id, cart_item_id):

    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

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
