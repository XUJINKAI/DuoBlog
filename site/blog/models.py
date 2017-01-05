from django.db import models
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.html import escape, strip_tags

from taggit.managers import TaggableManager

from . import managers

# Create your models here.
POST_VISIBLITY = (
	('p', 'public'),
	('d', 'draft'),
	)
POST_CONTENT_TYPE = (
	('m', 'markdown'),
	('h', 'html'),
	)
POST_ABSTRACT_TRUNC = 300
POST_TITLE_TRUNC = 32


class Setting(models.Model):
	site = models.OneToOneField(Site, primary_key=True)

	blog_name = models.CharField(max_length=32, default=settings.BLOG_PROGRAM_NAME)
	blog_desc = models.CharField(max_length=140, default='')
	blog_nav_tags = models.CharField(max_length=256, default='')
	new_post_content_type = models.CharField(max_length=1, choices=POST_CONTENT_TYPE)

	google_analytics_id = models.CharField(max_length=16, null=True)
	disqus_id = models.CharField(max_length=32, null=True)


class Post(models.Model):
	slug = models.CharField(max_length=64, unique=True, \
		blank=True)
	site = models.ForeignKey(Site)

	author = models.ForeignKey(settings.AUTH_USER_MODEL)
	title = models.CharField(max_length=70, blank=True)
	abstract = models.TextField(blank=True)
	content = models.TextField()
	content_type = models.CharField(max_length=1, choices=POST_CONTENT_TYPE)

	tags = TaggableManager(blank=True)
	# django_comments
	show_comment = models.BooleanField(default=True)

	create_time = models.DateTimeField(auto_now_add=True)
	last_modified_time = models.DateTimeField(auto_now=True)
	modified_count = models.PositiveIntegerField(default=0)
	views_count = models.PositiveIntegerField(default=0)

	visible = models.CharField(max_length=1, choices=POST_VISIBLITY)
	sticky = models.BooleanField(default=False)

	objects = managers.PostManager()

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-last_modified_time']

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = str(self.id)
		self.abstract = strip_tags(self.content)[:POST_ABSTRACT_TRUNC].strip() + '...'
		if self.title.isspace() or self.title is '':
			self.title = self.abstract[:POST_TITLE_TRUNC].strip() + '...'
		self.title = self.title.strip()
		super(Post, self).save(*args, **kwargs)
