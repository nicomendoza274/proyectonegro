# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-04 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0013_auto_20161003_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleados',
            name='estado',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='empleados',
            name='dni',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
