# Generated by Django 5.1.1 on 2024-10-09 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_app', '0005_follow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='fabrice-villard-Jrl_UQcZqOc-unsplash.jpg', null=True, upload_to='profile_pictures/'),
        ),
    ]