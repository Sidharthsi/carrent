# Generated by Django 5.0.2 on 2024-02-27 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0011_alter_carrentalbooking2_back_license_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrentalbooking2',
            name='license_number',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
    ]
