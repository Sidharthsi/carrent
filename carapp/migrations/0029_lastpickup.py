# Generated by Django 5.0.2 on 2024-04-11 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0028_carpackagebooking_package_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='LastPickup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_date', models.DateField()),
            ],
        ),
    ]
