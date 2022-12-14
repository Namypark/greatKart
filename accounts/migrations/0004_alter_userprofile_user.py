# Generated by Django 4.1 on 2022-10-18 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_alter_userprofile_gender"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="users",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
