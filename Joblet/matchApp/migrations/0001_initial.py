from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('candidate', '0006_candidate_likes_alter_candidatelike_candidate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
