# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-03-13 05:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0007_auto_20170310_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='members',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
