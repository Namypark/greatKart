from django.contrib.auth.forms import UserCreationForm
from django import forms

from accounts.models import Account


class RegistrationForm(UserCreationForm):

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter password", "class": "form-control"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "confirm password", "class": "form-control"}
        )
    )

    class Meta:
        model = Account
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password1",
        ]

    def __init__(self, *args, **kwargs):
        # inherits the form (telling it the class we are modifying)
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # can set the classes one at a time or just use a for loop
        self.fields["first_name"].widget.attrs["placeholder"] = "Enter first Name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Enter last Name"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Enter phone number"
        self.fields["email"].widget.attrs["placeholder"] = "Enter Email Address"

        for field in self.fields:
            self.fields.get(field).widget.attrs["class"] = "form-control"
