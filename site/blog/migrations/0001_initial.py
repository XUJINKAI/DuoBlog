# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-02 19:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogSetting',
            fields=[
                ('key', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=64)),
            ],
        ),
    ]