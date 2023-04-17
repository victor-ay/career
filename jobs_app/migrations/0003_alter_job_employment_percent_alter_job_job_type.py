# Generated by Django 4.1.7 on 2023-03-25 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs_app', '0002_company_company_id_linkedin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='employment_percent',
            field=models.TextField(db_column='employment_percent', default='Full-time'),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.TextField(choices=[('On-site', 'On Site'), ('Remote', 'Remote'), ('Hybrid', 'Hybrid')], db_column='job_type', default='On-site'),
        ),
    ]