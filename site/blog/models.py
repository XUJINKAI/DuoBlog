from django.db import models
from django.db.models import Q, F
from django.conf import settings
from django.utils.html import escape, strip_tags
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save

import json
import datetime
from taggit.managers import TaggableManager

from . import managers
from . import shortcuts

# Create your models here.
BLOG_COMMENTS = (
	('a', 'Anyone'),
	('l', 'Login'),
	('x', 'Close'),
	('d', 'disqus'),
	)
POST_CONTENT_TYPE = (
	('m', 'markdown'),
	('h', 'html'),
	)
POST_STATUS = (
	('p', 'public'),
	('d', 'draft'),
	('t', 'trash'),
	)
POST_TITLE_TRUNC = 32

def DEFAULT_NAVS():
	return json.dumps([
		{'name': 'Work', 'url': '/posts/?tags=work'},
		{'name': 'Life', 'url': '#', 'sub': [
				{'name': 'Movie', 'url': '/posts/?tags=movie'},
				{'name': 'Anime', 'url': '/posts/?tags=anime'},
			]},
		{'name': 'Diary', 'url': '/posts/?tags=diary'},
		])


def get_random_id(length):
	return get_random_string(length=length, allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789')

class Blog(models.Model):
	domain = models.CharField(max_length=100, unique=True, \
		help_text="Only this domain can access this blog")
	name = models.CharField(max_length=50)

	theme = models.CharField(max_length=16, default='default')
	default_editor = models.CharField(max_length=1, choices=POST_CONTENT_TYPE, default='m')
	rss = models.BooleanField(default=True)
	sitemap = models.BooleanField(default=True)
	comments = models.CharField(max_length=1, choices=BLOG_COMMENTS, default='a')

	google_analytics_id = models.CharField(max_length=16, null=True, blank=True)
	disqus_id = models.CharField(max_length=32, null=True, blank=True)

	desc = models.CharField(max_length=140, default='this is my new blog via MultBlog', blank=True)
	navs = models.CharField(max_length=1024, default='', blank=True)
	'''
	html_header
	html_tail
	'''

	def __str__(self):
		return self.domain

	def save(self, *args, **kwargs):
		shortcuts.clear_cache()
		super().save(*args, **kwargs)

	@classmethod
	def create_new(cls):
		domain = get_random_id(8)
		blog = Blog.objects.create(domain=domain, name='MultBlog', navs=DEFAULT_NAVS())
		return blog




class Post(models.Model):
	slug = models.CharField(max_length=128, unique=True, blank=True, \
		help_text="as post url")
	blog = models.ForeignKey(Blog)

	author = models.ForeignKey(settings.AUTH_USER_MODEL)
	title = models.CharField(max_length=70, blank=True)
	content = models.TextField()
	content_type = models.CharField(max_length=1, choices=POST_CONTENT_TYPE)

	tags = TaggableManager(blank=True)
	# django_comments
	comments = models.BooleanField(default=True)
	sticky = models.BooleanField(default=False)
	status = models.CharField(max_length=1, choices=POST_STATUS, default='d')

	create_time = models.DateTimeField(auto_now_add=True)
	last_modified_time = models.DateTimeField(auto_now=True)
	modified_count = models.PositiveIntegerField(default=0)
	views_count = models.PositiveIntegerField(default=0)

	objects = managers.PostManager()

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-create_time', '-last_modified_time']

	def save(self, *args, **kwargs):
		if self.title.isspace() or self.title is '':
			self.title = strip_tags(self.content)[:POST_TITLE_TRUNC].strip() + '...'
		self.title = self.title.strip()
		if self.slug.isspace() or self.slug is '':
			self.slug = self.get_auto_slug()
		self.last_modified_time = datetime.datetime.now()
		# F() expressions can only be used to update, not to insert.
		if self.pk is not None:
			self.modified_count = F('modified_count') + 1
		super(Post, self).save(*args, **kwargs)

	@staticmethod
	def get_auto_slug():
		return slugify(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '-' + get_random_id(4))


class Page(models.Model):
	blog = models.ForeignKey(Blog)
	url = models.CharField(max_length=128)

	title = models.CharField(max_length=70)
	content = models.TextField()
	comments = models.BooleanField(default=False)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.url = self.url.strip('/')
		if self.pk is None:
			find = Page.objects.filter(blog=self.blog, url=self.url)
			if len(find) > 0:
				raise Exception('already exists.')
		super(Page, self).save(*args, **kwargs)