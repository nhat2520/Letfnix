# Generated by Django 5.0.6 on 2024-05-20 16:05

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_cart_cart_id_alter_category_category_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='image',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='amount',
        ),
        migrations.AddField(
            model_name='movie',
            name='backdrop_path',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='poster_path',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='cart_id',
            field=models.UUIDField(default=uuid.UUID('b9883959-2616-435f-938e-177948635f62'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_id',
            field=models.UUIDField(default=uuid.UUID('de2b98b4-0d3d-478d-b19e-5416f0ac80e3'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('SF', 'Science Fiction'), ('ADV', 'Adventure'), ('ACT', 'Action'), ('FAN', 'Fantasy'), ('COM', 'Comedy'), ('DRA', 'Drama'), ('THR', 'Thriller'), ('CRI', 'Crime'), ('WAR', 'War'), ('MYS', 'Mystery'), ('HOR', 'Horror')]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_id',
            field=models.UUIDField(default=uuid.UUID('164a8203-8446-496d-913a-b0a1f45786a2'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='favorite_list',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.customer'),
        ),
        migrations.AlterField(
            model_name='favorite_list',
            name='favorite_list_id',
            field=models.UUIDField(default=uuid.UUID('af39a36f-9242-4630-b19e-ba5a3cc70d81'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='favorite_list',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='app.favorite_list'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='movie_id',
            field=models.UUIDField(default=uuid.UUID('19b2f9d9-4e59-4be7-bd3a-22611f3e5897'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.UUIDField(default=uuid.UUID('6c7a8631-0114-4f16-9c80-02fa57527e7b'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_id',
            field=models.UUIDField(default=uuid.UUID('435daa46-1092-438b-bb53-807ce75b79eb'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('PP', 'PayPal'), ('ST', 'STRIPE')]),
        ),
    ]