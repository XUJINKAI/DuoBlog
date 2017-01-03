from django.db import models
from django.contrib.sites.models import Site
from django.conf import settings

from taggit.managers import TaggableManager

# Create your models here.
COMMENT_CHOICES = (
	('i', 'buildin'),
	('d', 'disqus'),
	)
POST_VISIBLITY = (
	('p', 'public'),
	('l', 'login'),
	('s', 'staff'),
	('d', 'draft'),
	)
POST_CONTENT_TYPE = (
	('m', 'markdown'),
	('h', 'html'),
	)

class Setting(models.Model):
	site = models.ForeignKey(Site)
	blog_name = models.CharField(max_length=32, default=settings.BLOG_PROGRAM_NAME)
	blog_desc = models.CharField(max_length=140, default='')
	blog_nav_tags = models.CharField(max_length=256, default='')

	google_analytics_id = models.CharField(max_length=16, null=True)

	comment_system = models.CharField(max_length=1, choices=COMMENT_CHOICES)
	disqus_id = models.CharField(max_length=32)

	new_post_content_type = models.CharField(max_length=1, choices=POST_CONTENT_TYPE)
# flatpage
# https://docs.djangoproject.com/en/dev/ref/contrib/flatpages/?from=olddocs
	about_page_html = models.TextField(default='')


class Post(models.Model):
	slug = models.CharField(max_length=64, unique=True, \
		blank=True)

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

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.content = xssfilter(self.content)
		self.abstract = strip_tags(self.content)[:POST_ABSTRACT_TRUNC].strip() + '...'
		if self.title.isspace() or self.title is '':
			self.title = self.abstract[:POST_TITLE_TRUNC].strip() + '...'
		self.title = self.title.strip()
		super(Post, self).save(*args, **kwargs)

	class Meta:
		ordering = ['-last_modified_time']
