# Generated by Django 4.1.1 on 2024-10-18 09:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0013_alter_profile_city_alter_profile_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemsonstock',
            name='quantity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
