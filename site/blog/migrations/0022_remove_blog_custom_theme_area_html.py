# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-12 12:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_auto_20170311_0817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='custom_theme_area_html',
        ),
    ]
