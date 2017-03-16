from django.db import models as db_models
from django.db.models import Q
from .shortcuts import get_current_blog
from . import models as models


class PostManager(db_models.Manager):

	def guest_queryset(self, request, **kwargs):
		'''frontend'''
		current_blog = get_current_blog(request)
		return self.filter(blog=current_blog, deleted=False).exclude(status='x')

	def guest_home_queryset(self, request, **kwargs):
		'''frontend'''
		return self.guest_queryset(request, **kwargs).exclude(status='h') # h for hidden for home


class TagsManager(db_models.Manager):
	pass

class CommentsManager(db_models.Manager):
	pass