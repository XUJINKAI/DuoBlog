# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-07 06:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('blog', '0001_initial'), ('blog', '0002_auto_20170103_1954'), ('blog', '0003_auto_20170105_2350'), ('blog', '0004_auto_20170106_0103'), ('blog', '0005_auto_20170106_0103'), ('blog', '0006_auto_20170106_0106'), ('blog', '0007_auto_20170106_0119'), ('blog', '0008_auto_20170106_0128'), ('blog', '0009_auto_20170106_1920'), ('blog', '0010_auto_20170106_2138'), ('blog', '0011_auto_20170107_0024'), ('blog', '0012_blog_domain'), ('blog', '0013_auto_20170107_1157'), ('blog', '0014_auto_20170107_1418'), ('blog', '0015_auto_20170107_1420'), ('blog', '0016_auto_20170107_1420')]

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(blank=True, max_length=64, unique=True)),
                ('title', models.CharField(blank=True, max_length=70)),
                ('abstract', models.TextField(blank=True)),
                ('content', models.TextField()),
                ('content_type', models.CharField(choices=[('m', 'markdown'), ('h', 'html')], max_length=1)),
                ('show_comment', models.BooleanField(default=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('last_modified_time', models.DateTimeField(auto_now=True)),
                ('modified_count', models.PositiveIntegerField(default=0)),
                ('views_count', models.PositiveIntegerField(default=0)),
                ('visible', models.CharField(choices=[('p', 'public'), ('l', 'login'), ('s', 'staff'), ('d', 'draft')], max_length=1)),
                ('sticky', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-last_modified_time'],
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('desc', models.CharField(blank=True, default='', max_length=140)),
                ('google_analytics_id', models.CharField(blank=True, max_length=16, null=True)),
                ('disqus_id', models.CharField(blank=True, max_length=32, null=True)),
                ('default_editor', models.CharField(choices=[('e', 'Editor.md'), ('m', 'marked.js'), ('h', 'html')], default='e', max_length=1)),
                ('site', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='sites.Site')),
                ('rss', models.BooleanField(default=True)),
                ('sitemap', models.BooleanField(default=True)),
                ('theme', models.CharField(default='default', max_length=16)),
                ('pages_url_prefix', models.CharField(default='pages', max_length=12)),
                ('posts_url_prefix', models.CharField(default='posts', max_length=12)),
                ('navs', models.CharField(blank=True, default='', max_length=1024)),
                ('_domain', models.CharField(max_length=100, unique=True)),
                ('_name', models.CharField(default=1, max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='site',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sites.Site'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='visible',
            field=models.CharField(choices=[('p', 'public'), ('d', 'draft')], max_length=1),
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-last_modified_time', 'create_time']},
        ),
        migrations.RenameField(
            model_name='post',
            old_name='show_comment',
            new_name='comments',
        ),
        migrations.RemoveField(
            model_name='post',
            name='abstract',
        ),
        migrations.RemoveField(
            model_name='post',
            name='visible',
        ),
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('p', 'public'), ('d', 'draft')], default='d', max_length=1),
        ),
        migrations.AlterField(
            model_name='post',
            name='content_type',
            field=models.CharField(choices=[('e', 'Editor.md'), ('m', 'marked.js'), ('h', 'html')], max_length=1),
        ),
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
