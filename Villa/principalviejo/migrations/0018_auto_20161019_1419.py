# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-19 14:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0017_auto_20161019_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copia_detprod',
            name='articulo_reg2',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='copia_detprod',
            name='cantidad2',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='copia_detprod',
            name='capacidad2',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='copia_detprod',
            name='deposito2',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='copia_detprod',
            name='lote2',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='copia_detprod',
            name='tipo_reg2',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='detalle_produccion',
            name='cantidad',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='detalle_produccion',
            name='capacidad',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='detalle_produccion',
            name='deposito',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='detalle_produccion',
            name='lote',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='detalle_produccion',
            name='tipo_reg',
            field=models.IntegerField(default=0),
        ),
    ]