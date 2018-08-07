# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-19 23:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0019_auto_20161019_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido_reparto',
            name='ped_id',
        ),
        migrations.RemoveField(
            model_name='pedido_reparto',
            name='rep_id',
        ),
        migrations.RemoveField(
            model_name='repartos',
            name='cam_id',
        ),
        migrations.RemoveField(
            model_name='repartos',
            name='emp_id',
        ),
        migrations.AddField(
            model_name='pedidos',
            name='rep_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='repartidor', to='principal.Empleados'),
        ),
        migrations.DeleteModel(
            name='Pedido_Reparto',
        ),
        migrations.DeleteModel(
            name='Repartos',
        ),
    ]
