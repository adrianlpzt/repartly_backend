# Generated by Django 5.2.1 on 2025-06-08 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0003_profile_nif'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_admin_panel',
            field=models.BooleanField(default=False),
        ),
    ]
