# Generated by Django 5.1.3 on 2024-11-11 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_followermodel'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='followermodel',
            unique_together={('user', 'to_user')},
        ),
    ]
