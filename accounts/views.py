from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

# from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

from carts.models import CartItem

# from accounts.models import Account
from .models import Account
from .forms import RegistrationForm

# Create your views here.


@csrf_protect
def register(request):

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            # # * trying to use signals to make the code cleaner
            # email = form.cleaned_data["email"]
            # last_name = form.cleaned_data["last_name"]
            # first_name = form.cleaned_data["first_name"]
            # phone_number = form.cleaned_data["phone_number"]
            # password = form.cleaned_data["password1"]
            # username = email.split("@")[0]

            # user = Account.objects.create_user(
            #     first_name=first_name,
            #     last_name=last_name,
            #     username=username,
            #     email=email,
            #     password=password,
            # )
            # user.phone_number = phone_number
            user = form.save(commit=False)
            user.username = user.email.split("@")[0]
            email = user.email
            user.save()

            # SEND USER ACTIVATION MAIL

            current_site = get_current_site(request)
            subject = "GREATKART ACCOUNT ACTIVATION "
            """
           "urlsafe_base64_encode" takes user id and generates the base64 code(uidb64)  
           "default_token_generator.make_token" takes the user object and generates the onetime usable token for the user(token)
           " we create activation email using uidb64 and token and send it to user's email.
           " after clicking the activation url it will dispatched to the "activate_user_account" view
           " Here we receive "uidb64", "token". By using the "urlsafe_base64_decode" we decode the base64 encoded "uidb64" user id. We query the database with user id to get user.
           " We check the token validation using "default_token_generator.check_token" and "user object"

            """
            message = render_to_string(
                "accounts/account_verification_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            send_email = EmailMessage(subject, message, to=[email])
            send_email.send()
            # messages.success(request, "Please verify your account via the email sent to you to proceed.")
            return redirect("/accounts/login/?command=verification&email=" + email)

        else:
            messages.error(request, "Error registering account")
    else:
        messages.info(request, "please register here")
        form = RegistrationForm()

    context = {"form": form}
    return render(request, "accounts/register.html", context)


def activate(request, uidb64, token):
    print("ok")
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        print(f" this is the uid: {uid}")
        print(f" this is the user: {user}")
        user.is_active = True
        user.save()
        messages.success(request, "your account has been activated")
        return redirect("login")
        # return redirect('home')

    else:
        messages.error(request, "invalid activation link")
        return redirect("register")


@csrf_protect
def loginUser(request):
    if request.user.is_authenticated:
        return redirect("store")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = Account.objects.get(email=email)
        except:
            messages.error(request, "email does not exist")
            return redirect("login")

        user = authenticate(request, email=email, password=password)

        if user is not None:

            login(request, user)
            messages.success(request, "successfully logged in!")
            return redirect("dashboard")
        else:
            messages.error(
                request, "username or password is not correct please try again"
            )

    return render(request, "accounts/signin.html")


@login_required(login_url="login")
@csrf_protect
def logoutUser(request):
    logout(request)
    messages.info(request, "user logged out successfully")
    return redirect("login")


@login_required(login_url="login")
def dashboard(request):
    # if request.user.is_authenticated:
    #     order = CartItem.objects.get()
    return render(request, "accounts/dashboard.html")
