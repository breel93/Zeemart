# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-08 18:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_auto_20180907_1809'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=120, unique=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
    ]