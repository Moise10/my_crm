# Generated by Django 3.2.4 on 2021-06-29 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_agent_lead'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_agent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_organiser',
            field=models.BooleanField(default=True),
        ),
    ]
