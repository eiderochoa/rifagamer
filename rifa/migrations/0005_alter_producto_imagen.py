# Generated by Django 4.1.3 on 2023-01-19 16:23

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('rifa', '0004_alter_cuentabanco_num_cuenta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=95, scale=None, size=[950, 670], upload_to='productosimg/'),
        ),
    ]
