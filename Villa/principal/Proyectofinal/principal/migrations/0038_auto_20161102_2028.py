# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-02 20:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0037_auto_20161101_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumos',
            name='nombre',
            field=models.CharField(default='-', max_length=30),
        ),
    ]
