# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-04-25 10:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0007_auto_20170324_0642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votingparams',
            name='comments',
            field=models.TextField(max_length=500),
        ),
    ]