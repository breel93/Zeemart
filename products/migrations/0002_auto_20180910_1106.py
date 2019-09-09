# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-10 15:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=120, unique=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('category', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Category')),
                ('subcategory', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='products.SubCategory')),
            ],
            options={
                'verbose_name': 'SubSubCategory',
                'verbose_name_plural': 'SubSubCategories',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='subsubcategory',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='SubSubCategory', to='products.SubSubCategory'),
        ),
    ]
