# Generated by Django 4.1.7 on 2023-04-12 08:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs_app', '0021_applicationflow_is_deleted_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationflow',
            name='status_updated',
        ),
        migrations.AddField(
            model_name='applicationflow',
            name='created_at',
            field=models.DateTimeField(blank=True, db_column='created_at', default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='applicationflow',
            name='updated_at',
            field=models.DateTimeField(blank=True, db_column='updated_at', null=True),
        ),
    ]