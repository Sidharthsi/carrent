# Generated by Django 5.0.2 on 2024-02-23 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0004_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrentalbooking1',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=10),
        ),
    ]
