from django.db import models
from django.db.models import Q, F
from django.conf import settings
from django.utils.html import escape, strip_tags
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save

import json
import datetime

from . import managers
from . import shortcuts
from . import validators

# Create your models here.
BLOG_ACCESS = (
	('a', 'Anyone'),
	('l', 'Login'),
	('x', 'Close'),
	('p', 'Password'),
	)
BLOG_COMMENTS = (
	('a', 'Anyone'),
	('l', 'Login'),
	('x', 'Close'),
	('c', 'Custom'),
	)

POST_CONTENT_TYPE = (
	('m', 'markdown'),
	('h', 'html'),
	)
POST_STATUS = (
	('s', 'sticky'),
	('p', 'public'),
	('h', 'hidden'),
	('x', 'private'),
	)
POST_TITLE_TRUNC = 32

TAG_TYPE = (
	('u', 'User tag'),
	('s', 'System auto tag')
	)

def DEFAULT_NAVS():
	return json.dumps([])
	# example
	return json.dumps([
		# //TODO post.pk or url
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
	accessibility = models.CharField(max_length=1, choices=BLOG_ACCESS, default='a')
	password_hash = models.CharField(max_length=20, default='', blank=True, \
		help_text='Need if accessibility=p')
	domain = models.CharField(max_length=100, unique=True, \
		help_text="Only this domain can access this blog, e.g. emample.com")
	absolute_url = models.CharField(max_length=128, default='', validators=[validators.validate_abosolute_url], \
		help_text="To generate sitemap link, e.g. http://example.com/")

	name = models.CharField(max_length=50)
	desc = models.CharField(max_length=140, default='This is my new blog.', blank=True, \
		help_text='HTML')
	navs = models.TextField(default='[]', blank=True)
	theme = models.CharField(max_length=16, default='default')

	rss = models.BooleanField(default=True)
	sitemap = models.BooleanField(default=True)
	
	comments = models.CharField(max_length=1, choices=BLOG_COMMENTS, default='a')
	custom_comment_html = models.TextField(default='', blank=True, \
		help_text='work if comments=c')

	head_html = models.TextField(default='', blank=True, \
		help_text='insert to tail of head')
	body_html = models.TextField(default='', blank=True, \
		help_text='insert to tail of body')


	def __str__(self):
		return self.domain

	def save(self, *args, **kwargs):
		shortcuts.clear_cache()
		super().save(*args, **kwargs)

	@classmethod
	def create_new(cls):
		domain = get_random_id(50)
		name = 'DuoBlog_' + get_random_id(3)
		blog = Blog.objects.create(domain=domain, name=name, navs=DEFAULT_NAVS())
		return blog

	def post_count(self):
		return Post.objects.filter(blog=self, deleted=False).count()
	def trash_count(self):
		return Post.objects.filter(blog=self, deleted=True).count()
	def comment_count(self):
		return 0



class Post(models.Model):
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
	slug = models.CharField(max_length=128, unique=True, blank=True, \
		help_text="as url")

	title = models.CharField(max_length=70, blank=True, default='')
	content = models.TextField(default='')
	content_type = models.CharField(max_length=1, choices=POST_CONTENT_TYPE)
	rendered_html = models.TextField(default='')
	template_name = models.CharField(max_length=24, default='default')

	status = models.CharField(max_length=1, choices=POST_STATUS, default='x')
	deleted = models.BooleanField(default=False)
	comment_enable = models.BooleanField(default=True)

	create_time = models.DateTimeField(auto_now_add=True)
	last_modified_time = models.DateTimeField(auto_now=True)
	modified_count = models.PositiveIntegerField(default=0)
	views_count = models.PositiveIntegerField(default=0)
	like_count = models.PositiveIntegerField(default=0)

	objects = managers.PostManager()
	tags = managers.TagsManager()
	comments = managers.CommentsManager()

	def __str__(self):
		return self.title

	@property
	def is_public(self):
		return self.status is not 'x'

	def abstract(self):
		if self.title.isspace() or self.title is '':
			return strip_tags(self.rendered_html)[:POST_TITLE_TRUNC].strip() + '...'
		else:
			return self.title

	def absolute_url(self):
		return self.blog.absolute_url + settings.POSTS_URL_FIELD + '/' + self.slug

	class Meta:
		ordering = ['-create_time', '-last_modified_time']

	def save(self, *args, **kwargs):
		self.title = self.title.strip()
		if self.slug.isspace() or self.slug is '':
			self.slug = self.get_auto_slug()
		self.last_modified_time = datetime.datetime.now()
		if self.content_type == 'h':
			self.content = ''
		# F() expressions can only be used to update, not to insert.
		if self.pk is not None:
			self.modified_count = F('modified_count') + 1
		super(Post, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		if self.deleted:
			super(Post, self).delete(*args, **kwargs)
		else:
			self.deleted = True
			self.save()

	def restore(self):
		self.deleted = False
		self.save()

	@staticmethod
	def get_auto_slug():
		return slugify(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '-' + get_random_id(4))


class Tag(models.Model):
	post = models.ManyToManyField(Post)
	name = models.CharField(max_length=42, unique=True)
	tag_type = models.CharField(max_length=1, choices=TAG_TYPE, default='u')


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	login_user = models.ForeignKey(settings.AUTH_USER_MODEL, \
		on_delete=models.SET_NULL, null=True, blank=True)
	
	username = models.CharField(max_length=64)
	email = models.EmailField()
	website = models.CharField(max_length=64, default='')

	content = models.TextField()