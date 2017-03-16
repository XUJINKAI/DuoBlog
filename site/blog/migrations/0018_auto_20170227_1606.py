# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-27 08:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20170115_0119'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='rendered_html',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='default_editor',
            field=models.CharField(choices=[('m', 'markdown'), ('h', 'html')], default='m', max_length=1),
        ),
        migrations.AlterField(
            model_name='blog',
            name='desc',
            field=models.CharField(blank=True, default='this is my new blog via DuoBlog', max_length=140),
        ),
        migrations.AlterField(
            model_name='page',
            name='comments',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='content_type',
            field=models.CharField(choices=[('m', 'markdown'), ('h', 'html')], max_length=1),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('p', 'public'), ('d', 'draft'), ('t', 'trash')], default='d', max_length=1),
        ),
    ]
