# Generated by Django 5.1.1 on 2024-10-09 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0005_rename_saved_at_savedpost_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='draft',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]