# Generated by Django 4.2.5 on 2023-10-29 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_cart_cartdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartdetail',
            name='total',
            field=models.FloatField(blank=True, null=True),
        ),
    ]