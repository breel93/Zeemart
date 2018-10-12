# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-10-01 01:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_subsubcategory_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='descriptions',
            field=models.CharField(blank=True, max_length=120, unique=True),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='descriptions',
            field=models.CharField(blank=True, max_length=120, unique=True),
        ),
        migrations.AddField(
            model_name='subsubcategory',
            name='descriptions',
            field=models.CharField(blank=True, max_length=120, unique=True),
        ),
    ]
