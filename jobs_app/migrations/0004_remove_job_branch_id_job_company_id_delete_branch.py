# Generated by Django 4.1.7 on 2023-03-25 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs_app', '0003_alter_job_employment_percent_alter_job_job_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='branch_id',
        ),
        migrations.AddField(
            model_name='job',
            name='company_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.RESTRICT, to='jobs_app.company'),
        ),
        migrations.DeleteModel(
            name='Branch',
        ),
    ]
