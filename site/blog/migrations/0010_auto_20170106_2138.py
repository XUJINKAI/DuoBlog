# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-06 13:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20170106_1920'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-create_time', '-last_modified_time']},
        ),
        migrations.RemoveField(
            model_name='post',
            name='site',
        ),
        migrations.AddField(
            model_name='post',
            name='blog',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blog.Blog'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.CharField(blank=True, help_text='as post url', max_length=64, unique=True),
        ),
    ]
