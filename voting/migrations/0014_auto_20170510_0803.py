# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-05-10 08:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0013_booth_quarter'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quartersummary',
            options={'verbose_name': 'Quarter', 'verbose_name_plural': 'Quarter'},
        ),
        migrations.AddField(
            model_name='quartersummary',
            name='quarter_name',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
