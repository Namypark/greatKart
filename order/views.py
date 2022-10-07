import json
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


# Create your views here.
# models from cart
from carts.models import Cart, CartItem
from carts.views import _cart_id
from .forms import OrderForm
from .models import Order, Payment


@login_required(login_url="login")
def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_id=body["orderID"]
    )
    print(body)
    print("------------------------")
    print(order)
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

    return render(request, "order/payments.html")


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
