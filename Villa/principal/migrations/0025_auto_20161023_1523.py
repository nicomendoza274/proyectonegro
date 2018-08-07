# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-23 15:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0024_auto_20161023_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venta_sinpedido',
            name='fecha',
        ),
        migrations.AddField(
            model_name='ventas',
            name='fecha',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='ventas',
            name='pedido',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='principal.Pedidos'),
        ),
    ]