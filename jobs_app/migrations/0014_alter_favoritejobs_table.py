# Generated by Django 4.1.7 on 2023-04-08 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs_app', '0013_favoritejobs'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='favoritejobs',
            table='favorite_jobs',
        ),
    ]