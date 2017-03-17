# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-16 05:33
from __future__ import unicode_literals

import blog.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_auto_20170315_0048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='sticky',
        ),
        migrations.AddField(
            model_name='post',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='blog',
            name='absolute_url',
            field=models.CharField(default='', help_text='To generate sitemap link, e.g. http://example.com/', max_length=128, validators=[blog.validators.validate_abosolute_url]),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('s', 'sticky'), ('p', 'public'), ('h', 'hidden'), ('r', 'private')], default='r', max_length=1),
        ),
    ]