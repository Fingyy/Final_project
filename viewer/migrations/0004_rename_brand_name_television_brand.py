# Generated by Django 4.1.1 on 2024-10-06 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0003_category_profile_television_categories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='television',
            old_name='brand_name',
            new_name='brand',
        ),
    ]
