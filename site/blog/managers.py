from django.db import models as db_models
from django.db.models import Q
from .shortcuts import get_current_blog
from . import models


class PostManager(db_models.Manager):

	def guest_queryset(self, request, **kwargs):
		'''frontend'''
		current_blog = get_current_blog(request)
		return self.filter(blog=current_blog, deleted=False).exclude(status='x')

	def guest_home_queryset(self, request, **kwargs):
		'''frontend'''
		return self.guest_queryset(request, **kwargs).exclude(status='h') # h for hidden for home


# class TagsManager(db_models.manager.BaseManager.from_queryset(Tag)):
	
# 	def __str__(self):
# 		return 'dddddddddd'


# 	def add(self, tag):
# 		pass

# 	def all(self):
# 		pass

# 	def remove(self, tag):
# 		pass
		


class CommentsManager(db_models.Manager):
	pass