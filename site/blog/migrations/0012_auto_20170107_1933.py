# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-07 11:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20170107_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='domain',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
