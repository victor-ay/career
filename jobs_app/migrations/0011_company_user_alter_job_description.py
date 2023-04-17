# Generated by Django 4.1.7 on 2023-03-27 16:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs_app', '0010_remove_job_currency_remove_job_currency_currency_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.TextField(blank=True, db_column='description', max_length='65536', null=True),
        ),
    ]