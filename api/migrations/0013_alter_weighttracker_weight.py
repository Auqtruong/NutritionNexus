# Generated by Django 5.1.3 on 2025-01-28 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_food_name_alter_user_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weighttracker',
            name='weight',
            field=models.DecimalField(decimal_places=1, max_digits=6),
        ),
    ]
