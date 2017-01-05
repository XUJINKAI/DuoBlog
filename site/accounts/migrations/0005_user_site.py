# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-05 15:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('accounts', '0004_remove_user_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='site',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sites.Site'),
            preserve_default=False,
        ),
    ]
