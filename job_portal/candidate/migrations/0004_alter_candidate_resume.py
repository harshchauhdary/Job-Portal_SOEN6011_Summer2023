# Generated by Django 4.2.3 on 2023-07-18 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0003_candidate_delete_app_user_remove_job_position_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='resume',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='candidate.resume'),
        ),
    ]
