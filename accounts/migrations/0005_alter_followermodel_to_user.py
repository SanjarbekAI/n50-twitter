# Generated by Django 5.1.3 on 2024-11-13 12:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_followermodel_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followermodel',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]