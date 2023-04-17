# Generated by Django 4.1.7 on 2023-03-25 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs_app', '0007_alter_job_employment_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='application_url',
            field=models.TextField(blank=True, db_column='application_url', max_length='2048', null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='location',
            field=models.TextField(blank=True, db_column='location', max_length='1024', null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='posted_on_epoch',
            field=models.IntegerField(blank=True, db_column='posted_on_epoch', null=True),
        ),
    ]