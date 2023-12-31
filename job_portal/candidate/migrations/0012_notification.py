# Generated by Django 4.2.3 on 2023-08-01 02:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0011_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('read', models.BooleanField(default=False)),
                ('candidate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='candidate.candidate')),
            ],
        ),
    ]
