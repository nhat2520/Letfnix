# Generated by Django 5.0.6 on 2024-05-24 14:24

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_cart_cart_id_alter_customer_customer_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_id',
            field=models.UUIDField(default=uuid.UUID('0d587ad4-3da9-48db-8940-8fe9ef4a3038'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_id',
            field=models.UUIDField(default=uuid.UUID('be414d45-d0fb-4164-b827-c851e0946e66'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='favorite_list',
            name='favorite_list_id',
            field=models.UUIDField(default=uuid.UUID('6c4c2407-cb6f-4e44-b812-0cf5881bf241'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='movie_id',
            field=models.UUIDField(default=uuid.UUID('f31dafb9-a339-4b2d-9932-758f9b2a9d0b'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.UUIDField(default=uuid.UUID('3a25ed95-0614-4962-aa4e-0096bdee3fba'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_id',
            field=models.UUIDField(default=uuid.UUID('f3e87579-8a15-4035-a499-3cac5a6c2c4d'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
