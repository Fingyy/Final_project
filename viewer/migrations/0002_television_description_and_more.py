# Generated by Django 4.1.1 on 2024-09-19 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='television',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='tvdisplaytechnology',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]