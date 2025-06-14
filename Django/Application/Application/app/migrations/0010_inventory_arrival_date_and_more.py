# Generated by Django 5.0.6 on 2025-06-06 09:46

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_inventory_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='arrival_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='inventory',
            name='estimated_expiration_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inventory',
            name='estimated_expiration_week',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='inventory',
            name='shelf_life',
            field=models.PositiveIntegerField(default=7),
        ),
        migrations.AddField(
            model_name='inventory',
            name='status',
            field=models.CharField(default='Fresh', max_length=20),
        ),
    ]
