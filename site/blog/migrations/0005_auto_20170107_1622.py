# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-07 08:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20170107_1526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='id',
        ),
        migrations.AlterField(
            model_name='blog',
            name='domain',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
