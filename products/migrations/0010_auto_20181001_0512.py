# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-10-01 09:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20181001_0509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='old_price',
            field=models.DecimalField(blank=True, decimal_places=0, default=0.0, max_digits=10, null=True),
        ),
    ]
