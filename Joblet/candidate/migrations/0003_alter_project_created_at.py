# Generated by Django 5.1.2 on 2024-12-13 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0002_candidate_approved_candidate_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]