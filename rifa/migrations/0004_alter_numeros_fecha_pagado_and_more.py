# Generated by Django 4.1.3 on 2022-11-24 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rifa', '0003_rifa_stado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numeros',
            name='fecha_pagado',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='numeros',
            name='fecha_seleccionado',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
