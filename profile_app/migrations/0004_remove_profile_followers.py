# Generated by Django 5.1.1 on 2024-10-09 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile_app', '0003_alter_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='followers',
        ),
    ]
