from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password):
        if not email:
            raise ValueError("You must have an email address")

        if not username:
            raise ValueError("You do not have a username")

        user = self.model(
            email=self.normalize_email(
                email
            ),  # changes capital to small letter incase you put a capital there.
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        # The set_password is an inbuilt function
        user.set_password(password)
        user.save(using=self._db)
        return user

    # creating a superuser with the create user method we created first above
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        # can be gotten from the django admin as well
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True

        user.save(using=self._db)
        return user


# This was created fist but without making migrations then MYACCOUNTMANAGER 2ND
class Account(AbstractBaseUser):
    first_name = models.CharField(
        max_length=50,
    )
    last_name = models.CharField(
        max_length=50,
    )
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.IntegerField(null=True)

    # Date registered
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    # permissions
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
