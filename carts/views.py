from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from store.models import Product, Variation


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()

    return cart


def add_cart(request, product_id):
    # ? getting current user
    current_user = request.user
    # getting the product here using the product id
    product = Product.objects.get(id=product_id)
    # getting the product variation here
    product_variation = []
    variation = ""
    # if the request is a post request we loop the item(s) and assign them the variable KEY
    #! AUTHENTICATED-->
    if current_user.is_authenticated:

        if request.method == "POST":
            for item in request.POST:
                key = item
                # we get the value for the responding key elements(as in a dict)
                # ex: if the item is 'color' it is assigned to the key variable
                # then the value for the key is provided hence 'red,blue' etc
                value = request.POST.get(key)

                # WE get the variation objects by filtering by the product we got
                # and the variation category (key) and the value(value)
                try:
                    variation = Variation.objects.get(
                        product=product,
                        variation_category__iexact=key,
                        variation_value__iexact=value,
                    )
                    # we append the variation inside the list ie [product,color(blue),size(medium)]
                    product_variation.append(variation)

                # if it is we  filter the cartItem, we make a empty list to hold the existing variation and ID
                except:
                    pass

        try:
            cart = Cart.objects.get(
                cart_id=_cart_id(request)
            )  # get the cart using the cart id present in the sessio
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        # if the cart does not exist we create the ca
        cart.save()

        is_cart_item_exist = CartItem.objects.filter(
            product=product, user=current_user
        ).exists()

        if is_cart_item_exist:
            cart_item = CartItem.objects.filter(product=product, user=current_user)

            existing_variation_list = []
            id = []
            # we loop through the cart item and for each item we get their variation
            # AND append that to the existing variation list and append the ID to the ID lis
            for item in cart_item:
                existing_variations = item.variations.all()
                existing_variation_list.append(list(existing_variations))
                id.append(item.id)

            # here we check for existing variation index in the product variation
            if product_variation in existing_variation_list:

                index = existing_variation_list.index(product_variation)
                # we get the index and the index of the item_id
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                # increase the cartItem quantity
                # we get the item from the item cartItem(with the product and item_id) and increase the quantity

                item.quantity += 1
                item.save()

            else:
                # if the existing variation is not in product_variation we create the item
                # create a new item
                item = CartItem.objects.create(
                    product=product,
                    quantity=1,
                    user=current_user,
                    cart=cart
                    # ? ran into some issues so i had to  add the cart(it wasnt added before because it kept raising ID issues)
                    # ? had to add the cart because of cart.id issues
                )
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()

        else:
            # we create the product if it does not exist and add the variations to it
            # ? had to add the cart because of cart.id issues

            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
                user=current_user,
            )
            ("here 2")
            if len(product_variation) > 0:
                cart_item.variations.clear
                cart_item.variations.add(*product_variation)
            cart_item.save
        return redirect("cart")

        #! NOT AUTHENTICATED -->
    else:

        if request.method == "POST":
            for item in request.POST:
                key = item
                # we get the value for the responding key elements(as in a dict)
                # ex: if the item is 'color' it is assigned to the key variable
                # then the value for the key is provided hence 'red,blue' etc
                value = request.POST.get(key)

                try:
                    variation = Variation.objects.get(
                        product=product,
                        variation_category__iexact=key,
                        variation_value__iexact=value,
                    )
                    # we append the variation inside the list ie [product,color(blue),size(medium)]
                    product_variation.append(variation)
                # if it is we filter the cartItem, we make a empty list to hold the existing variation and ID
                except:
                    pass

        try:
            cart = Cart.objects.get(
                cart_id=_cart_id(request)
            )  # get the cart using the cart id present in the sessio
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        # if the cart does not exist we create the ca
        cart.save()
        # GETTING THE CART ITEM HERE
        # here we filter if the product is already in the cart(this returns a BOOL)
        is_cart_item_exist = CartItem.objects.filter(
            product=product, cart=cart
        ).exists()
        # if it is we filter the cartItem, we make a empty list to hold the existing variation and
        if is_cart_item_exist:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # existing variations --> Database
            # current variations --> product_variation
            # item id --> database
            existing_variation_list = []
            id = []
            # we loop through the cart item and for each item we get their variation
            # AND append that to the existing variation list and append the ID to the ID li
            for item in cart_item:
                existing_variations = item.variations.all()
                existing_variation_list.append(list(existing_variations))
                id.append(item.id)
            # here we check for existing variation index in the product variation
            if product_variation in existing_variation_list:
                # increase the cartItem quantity
                index = existing_variation_list.index(product_variation)
                # we get the index and the index of the item_id
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                # we get the item from the item cartItem(with the product and item_id) and increase the quanti
                item.quantity += 1
                item.save()
            else:
                # if the existing variation is not in product_variation we create the item
                # create a new item
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            # we create the product if it does not exist and add the variations to it
            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                cart_item.variations.clear
                cart_item.variations.add(*product_variation)
            cart_item.save
        return redirect("cart")

    # GETTING THE CART HERE


def remove_cart(request, product_id, cart_item_id):
    # 1.) get the cart
    cart = Cart.objects.get(cart_id=_cart_id(request))
    # 2.) get the product by id
    product = get_object_or_404(Product, id=product_id)
    try:

        # 3.)get the cart item
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, user=request.user, id=cart_item_id
            )

        else:
            cart_item = CartItem.objects.get(
                product=product, cart=cart, id=cart_item_id
            )
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

    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, user=request.user, id=cart_item_id
            )
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(
                product=product, cart=cart, id=cart_item_id
            )
        if cart_item.quantity > 0:
            cart_item.delete()
    except:
        pass

    return redirect("cart")


def cart(request, total_price=0, quantity=0, cart_items=None):
    try:
        # ? CHECKING IF THE USER IS AUTHENTICATED SO WE CAN GET THE CART OFF THE USER
        # ? AND NOT OFF THE COOKIE SESSION
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
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


@login_required(login_url="login")
def checkout(request, total_price=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(is_active=True, user=request.user)
        else:
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
    return render(request, "carts/checkout.html", context)
