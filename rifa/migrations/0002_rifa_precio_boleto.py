# Generated by Django 4.1.3 on 2023-01-07 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rifa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rifa',
            name='precio_boleto',
            field=models.FloatField(default=199),
        ),
    ]
