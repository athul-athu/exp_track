# Generated by Django 4.2.6 on 2025-07-06 17:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_userdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='age',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='Age must be greater than 0'), django.core.validators.MaxValueValidator(150, message='Age must be less than 150')]),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='phone_number',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
