# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-06 19:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0003_auto_20160906_0345'),
    ]

    operations = [
        migrations.AddField(
            model_name='insumos',
            name='descripcion',
            field=models.CharField(default='-', max_length=60),
        ),
        migrations.AddField(
            model_name='insumos',
            name='existenciamin',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='insumos',
            name='nombre',
            field=models.CharField(default='-', max_length=30),
        ),
    ]
