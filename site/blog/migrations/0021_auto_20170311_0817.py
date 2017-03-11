# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-11 00:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_auto_20170311_0732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='password_hash',
            field=models.CharField(blank=True, default='', help_text='Need if accessibility=p', max_length=20),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=42, unique=True),
        ),
    ]
