# Generated by Django 4.1 on 2022-08-24 05:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="id",
            field=models.UUIDField(
                primary_key=True, serialize=False, verbose_name=uuid.uuid4
            ),
        ),
    ]
