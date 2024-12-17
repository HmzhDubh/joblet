# Generated by Django 5.1.2 on 2024-12-17 08:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('candidate', '0006_candidate_likes_alter_candidatelike_candidate'),
        ('organization', '0016_alter_organization_profile_completion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_match', models.BooleanField(default=False)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='candidate.candidate')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='organization.organization')),
            ],
        ),
    ]
