# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-03-13 07:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0010_auto_20170313_0747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='members',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teams.Teams'),
        ),
    ]