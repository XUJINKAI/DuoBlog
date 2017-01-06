from django.db import models
from django.db.models import Q, F
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.html import escape, strip_tags
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string

import datetime
from taggit.managers import TaggableManager

from . import managers

# Create your models here.
POST_STATUS = (
	('p', 'public'),
	('d', 'draft'),
	)
POST_CONTENT_TYPE = (
	('e', 'Editor.md'),
	('m', 'marked.js'),
	('h', 'html'),
	)
POST_TITLE_TRUNC = 32

def get_random_id(length):
	return get_random_string(length=length, allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789')


class Blog(models.Model):
	site = models.OneToOneField(Site, primary_key=True, on_delete=models.CASCADE)

	name = models.CharField(max_length=32, default=settings.BLOG_PROGRAM_NAME)
	desc = models.CharField(max_length=140, default='', blank=True)
	navs = models.CharField(max_length=1024, default='', blank=True)
	theme = models.CharField(max_length=16, default='default')

	default_editor = models.CharField(max_length=1, choices=POST_CONTENT_TYPE, default='e')
	posts_url_prefix = models.CharField(max_length=12, default='posts')
	pages_url_prefix = models.CharField(max_length=12, default='pages')

	google_analytics_id = models.CharField(max_length=16, null=True, blank=True)
	disqus_id = models.CharField(max_length=32, null=True, blank=True)

	rss = models.BooleanField(default=True)
	sitemap = models.BooleanField(default=True)


	def __str__(self):
		return self.name

	@classmethod
	def create(cls, site):
		blog = cls(site=site)
		return blog

class Post(models.Model):
	slug = models.CharField(max_length=64, unique=True, blank=True, \
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