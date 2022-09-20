from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings

## verify from email


from .models import Account

# ? signals help us give alert or perform specific actions when certain actions happen
@receiver(post_save, sender=Account)
def createProfile(sender, instance, created, **kwargs):

    if created:
        user = instance
        profile = Account.objects.create_user(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            password=user.password,
            username=user.email.split("@")[0],
        )
        user.phone_number = user.phone_number

        print("user created")
        user.save()


## ? signal to delete the user account
@receiver(post_delete, sender=Account)
def deleteUser(sender, instance, **kwargs):
    user = instance.user

    user.delete()
    print("Accounted deleted")
