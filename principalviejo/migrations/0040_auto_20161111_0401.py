# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-11 04:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0039_auto_20161106_2215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='copia_remitos',
            name='dep_id2',
        ),
        migrations.RemoveField(
            model_name='remitos',
            name='dep_id',
        ),
        migrations.AddField(
            model_name='copia_detrem',
            name='dep_id2',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='principal.Depositos'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detalle_remito',
            name='dep_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='principal.Depositos'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='copia_detrem',
            name='ins_id2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.Insumos'),
        ),
        migrations.AlterField(
            model_name='copia_remitos',
            name='prov_id2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.Proveedores'),
        ),
    ]