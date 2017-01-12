from django.db import models
from django.db.models import Q, F
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.utils.html import escape, strip_tags
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save

import datetime
from taggit.managers import TaggableManager

from . import managers

# Create your models here.
BLOG_COMMENTS = (
	('a', 'Anyone'),
	('l', 'Login'),
	('x', 'Close'),
	('d', 'disqus'),
	)
POST_STATUS = (
	('p', 'public'),
	('d', 'draft'),
	)
POST_CONTENT_TYPE = (
	('m', 'marked.js'),
	('h', 'html'),
	)
POST_TITLE_TRUNC = 32

def get_random_id(length):
	return get_random_string(length=length, allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789')

class Blog(models.Model):
	site = models.OneToOneField(Site, on_delete=models.CASCADE, to_field='id')
	domain = models.CharField(max_length=100, unique=True, \
		help_text="Only this domain can access this blog")
	name = models.CharField(max_length=50)

	desc = models.CharField(max_length=140, default='', blank=True)
	navs = models.CharField(max_length=1024, default='', blank=True)
	theme = models.CharField(max_length=16, default='default')

	default_editor = models.CharField(max_length=1, choices=POST_CONTENT_TYPE, default='m')
	posts_url_prefix = models.CharField(max_length=12, default='posts', help_text='//TODO')
	pages_url_prefix = models.CharField(max_length=12, default='pages', help_text='//TODO')

	google_analytics_id = models.CharField(max_length=16, null=True, blank=True)
	comments = models.CharField(max_length=1, choices=BLOG_COMMENTS, default='a')
	disqus_id = models.CharField(max_length=32, null=True, blank=True)

	rss = models.BooleanField(default=True)
	sitemap = models.BooleanField(default=True)

	def __str__(self):
		return self.domain

	def save(self, *args, **kwargs):
		site = self.related_site
		site.domain = self.domain
		site.name = self.name
		site.save()
		super().save(*args, **kwargs)

	@property
	def related_site(self):
		return self.site

	@classmethod
	def create_new(cls):
		domain = get_random_id(8)
		name = get_random_id(8)
		site = Site.objects.create(domain=domain, name=name)
		### blog will be create automatic cause signal connect site_post_save()
		### blog = Blog.objects.create(site=site, domain=domain, name=name)
		### NO need to create blog AGAIN
		return site.blog

	@staticmethod
	def get_or_create_by_site(site):
		if hasattr(site, 'blog'):
			return site.blog
		else:
			return Blog.objects.create(site=site, domain=site.domain, name=site.name)


# when create Site(), auto create related Blog()
def site_post_save(instance, create=None, raw=None, **kwargs):
	if not hasattr(instance, 'blog'):
		Blog.objects.create(site=instance, domain=instance.domain, name=instance.name)

post_save.connect(site_post_save, sender=Site)


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