# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-25 04:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20180922_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='old_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=20, null=True),
        ),
    ]
