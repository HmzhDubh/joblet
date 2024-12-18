# Generated by Django 5.1.2 on 2024-12-17 15:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0007_remove_candidate_likes_delete_candidatelike'),
        ('matchApp', '0004_remove_match_project_match_organization_and_more'),
        ('organization', '0016_remove_projects_likes_delete_organizationlike'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuperLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='candidate.candidate')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.organization')),
            ],
        ),
    ]