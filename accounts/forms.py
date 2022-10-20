import profile
from django.contrib.auth.forms import UserCreationForm
from django import forms

from accounts.models import Account, UserProfile


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


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            "first_name",
            "last_name",
            "phone_number",
        ]

    def __init__(self, *args, **kwargs):
        # inherits the form (telling it the class we are modifying)
        super(UserForm, self).__init__(*args, **kwargs)
        # can set the classes one at a time or just use a for loop
        self.fields["first_name"].widget.attrs["placeholder"] = "Enter first Name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Enter last Name"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Enter phone number"

        for field in self.fields:
            self.fields.get(field).widget.attrs["class"] = "form-control"


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False,
        error_messages={"invalid": ("Image files only")},
        widget=forms.FileInput,
    )

    class Meta:
        model = UserProfile

        fields = [
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "country",
            "gender",
            "profile_picture",
        ]

    def __init__(self, *args, **kwargs):
        # inherits the form (telling it the class we are modifying)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # can set the classes one at a time or just use a for loop
        self.fields["address_line_1"].widget.attrs["placeholder"] = "Enter Your Address"
        self.fields["address_line_2"].widget.attrs["placeholder"] = "Enter Your Address"
        self.fields["city"].widget.attrs["placeholder"] = "city"
        self.fields["country"].widget.attrs["placeholder"] = "country"

        for field in self.fields:
            self.fields.get(field).widget.attrs["class"] = "form-control"
