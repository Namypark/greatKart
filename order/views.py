import json
from multiprocessing import context
from os import stat
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from requests import request

# Create your views here.
# models from cart
from carts.models import Cart, CartItem
from carts.views import _cart_id
import order
from .forms import OrderForm

# models from order
from .models import Order, Payment, OrderProduct

# models from store
from store.models import Product


@login_required(login_url="login")
def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_id=body["orderID"]
    )

    payment = Payment(
        user=request.user,
        payment_id=body["transID"],
        payment_method=body["payment_method"],
        amount_paid=order.order_total,
        status=body["status"],
    )

    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    """
    1.) move items to the order product table
    2.) reduce the quantity of products in the store
    3.) clear cart
    4.) send user an email
    5.) send order number and trans id back to onapprove in html via JSONRESPONSE

    """
    # 1.)  move items to the order product table
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        # ? adding the orderproduct inside the loop helps make the order product add other items that are in the cart else it adds only the last item.
        order_product = OrderProduct()
        order_product.order_id = order.id
        # print(f"order_product.order_id={order_product.order_id}")
        order_product.payment = payment
        #
        order_product.user_id = request.user.id
        # print(f"order_product.user_id = {request.user.id}")
        order_product.product_id = item.product_id
        # print(f"order_product.quantity={item.quantity}")
        order_product.quantity = item.quantity
        order_product.product_price = item.product.price
        # print(f"order_product.product_price={item.product.price}")
        order_product.ordered = True
        # print(f"order_product.ordered={True}")
        order_product.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()

        order_product = OrderProduct.objects.get(id=order_product.id)
        order_product.variations.set(product_variation)
        order_product.save()
        # 2,)  reduce the quantity of products in the store
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
    # 3.) clear cart
    CartItem.objects.filter(user=request.user).delete()
    # 4.) send email to user
    subject = "Thank you for your order "
    user = request.user
    email = order.email
    message = render_to_string(
        "order/order_received_email.html",
        {
            "user": user,
            "order": order,
        },
    )
    send_email = EmailMessage(subject, message, to=[email])
    send_email.send()

    # -----><>
    OrderData = {"order_id": order.order_id, "transID": payment.payment_id}

    return JsonResponse(OrderData)


@login_required(login_url="login")
def place_order(request, total_price=0, quantity=0, total=0, tax=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect("store")
    for cart_item in cart_items:
        total_price += round(cart_item.product.price * cart_item.quantity, 2)
        quantity += cart_item.quantity
    tax = round((total_price * 2) / 100, 2)
    total = round(tax + total_price, 2)

    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            data = Order()
            data.user = request.user
            data.first_name = form.cleaned_data["first_name"]
            data.last_name = form.cleaned_data["last_name"]
            data.phone = form.cleaned_data["phone"]
            data.email = form.cleaned_data["email"]
            data.address_line_1 = form.cleaned_data["address_line_1"]
            data.address_line_2 = form.cleaned_data["address_line_2"]
            data.country = form.cleaned_data["country"]
            data.city = form.cleaned_data["city"]
            data.state = form.cleaned_data["state"]
            data.order_note = form.cleaned_data["order_note"]
            data.order_total = total
            data.tax = tax
            data.ip = request.META.get("REMOTE_ADDR")
            data.save()
            id = data.order_id
            order = Order.objects.get(user=current_user, is_ordered=False, order_id=id)
            context = {
                "order": order,
                "cart_items": cart_items,
                "total": total,
                "tax": tax,
                "total_price": total_price,
            }

            return render(request, "order/payments.html", context)
        else:
            return redirect("checkout")


def order_complete(request):

    order_id = request.GET.get("order_id")
    payment_id = request.GET.get("payment_id")
    print(order_id, payment_id)
    order = Order.objects.get(order_id=order_id, user=request.user)
    payment = Payment.objects.get(payment_id=payment_id, user=request.user)
    order_product = OrderProduct.objects.filter(order=order)

    sub_total = 0
    for total in order_product:
        sub_total += total.quantity * total.product_price

    context = {
        "order": order,
        "payment": payment,
        "order_product": order_product,
        "sub_total": sub_total,
    }

    return render(request, "order/order_complete.html", context)
