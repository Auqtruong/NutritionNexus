# Generated by Django 5.1.3 on 2025-02-11 20:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_alter_dailyintake_food_entry_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyintake',
            name='food_entry_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='weighttracker',
            name='weight_entry_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
