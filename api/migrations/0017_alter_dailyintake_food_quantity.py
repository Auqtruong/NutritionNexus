# Generated by Django 5.1.3 on 2025-01-30 19:03

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_dailyintake_food_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyintake',
            name='food_quantity',
            field=models.DecimalField(decimal_places=2, default=Decimal('100'), max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('1.0')), django.core.validators.MaxValueValidator(Decimal('1000.0'))]),
        ),
    ]
