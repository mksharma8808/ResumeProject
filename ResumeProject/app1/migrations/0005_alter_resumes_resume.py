# Generated by Django 5.0.3 on 2024-12-15 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_resumes_created_at_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resumes',
            name='resume',
            field=models.FileField(upload_to='resumes/'),
        ),
    ]
