# Generated by Django 4.1.1 on 2024-10-08 17:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0004_rename_brand_name_television_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='television',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='television_images/'),
        ),
        migrations.AddField(
            model_name='television',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]