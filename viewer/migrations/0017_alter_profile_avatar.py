# Generated by Django 4.1.1 on 2024-10-20 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0016_delete_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='media/avatars/profile_pic.png', null=True, upload_to='media/avatars/'),
        ),
    ]
