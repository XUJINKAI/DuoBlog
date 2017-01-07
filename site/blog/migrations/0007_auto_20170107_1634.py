# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-07 08:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('blog', '0006_auto_20170107_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='domain',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='id',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='name',
        ),
        migrations.AddField(
            model_name='blog',
            name='site_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sites.Site'),
            preserve_default=False,
        ),
    ]
