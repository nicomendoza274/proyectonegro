# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-01 22:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0011_pedidos_formapago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulos',
            name='nombre',
            field=models.CharField(default='-', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='insumos',
            name='nombre',
            field=models.CharField(default='-', max_length=30, unique=True),
        ),
    ]
