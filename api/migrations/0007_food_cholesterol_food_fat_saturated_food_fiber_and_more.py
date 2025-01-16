# Generated by Django 5.1.3 on 2025-01-11 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_dailyintake_calories_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='cholesterol',
            field=models.DecimalField(blank=True, decimal_places=1, default=None, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='food',
            name='fat_saturated',
            field=models.DecimalField(blank=True, decimal_places=1, default=None, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='food',
            name='fiber',
            field=models.DecimalField(blank=True, decimal_places=1, default=None, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='food',
            name='potassium',
            field=models.DecimalField(blank=True, decimal_places=1, default=None, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='food',
            name='serving_size',
            field=models.DecimalField(blank=True, decimal_places=1, default=None, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='food',
            name='sodium',
            field=models.DecimalField(blank=True, decimal_places=1, default=None, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='food',
            name='sugar',
            field=models.DecimalField(blank=True, decimal_places=1, default=None, max_digits=6, null=True),
        ),
    ]
