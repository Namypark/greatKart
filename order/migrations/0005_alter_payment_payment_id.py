# Generated by Django 4.1 on 2022-10-07 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0004_alter_order_payment_alter_order_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="payment_id",
            field=models.CharField(max_length=100),
        ),
    ]