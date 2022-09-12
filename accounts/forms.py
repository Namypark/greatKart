from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from accounts.models import Account


class RegistrationForm(UserCreationForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "confirm password",
            }
        )
    )

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "phone_number", "password"]

    def __init__(self, *args, **kwargs):
        # inherits the form (telling it the class we are modifying)
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # can set the classes one at a time or just use a for loop
        self.fields["first_name"].widget.attrs["placeholder"] = "Enter first Name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Enter last Name"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Enter phone number"
        self.fields["email"].widget.attrs.update({"placeholder": "Enter Email Address"})

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})
