# Generated by Django 4.2.5 on 2023-10-31 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sittings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deliveryfee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee', models.FloatField()),
            ],
        ),
    ]