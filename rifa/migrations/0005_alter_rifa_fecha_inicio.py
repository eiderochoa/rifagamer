# Generated by Django 4.0.3 on 2022-11-24 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rifa', '0004_alter_numeros_fecha_pagado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rifa',
            name='fecha_inicio',
            field=models.DateField(),
        ),
    ]