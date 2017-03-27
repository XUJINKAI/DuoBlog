from django.db import models as db_models
from django.db.models import Q
from .shortcuts import get_current_blog
from . import models as models


class PostManager(db_models.Manager):

	def guest_queryset(self, request, hidden=False, **kwargs):
		'''frontend'''
		current_blog = get_current_blog(request)
		status = ['s', 'p']
		if hidden:
			status += 'h'
		return self.filter(blog=current_blog, deleted=False, status__in=status)


class TagsManager(db_models.Manager):
	pass

class CommentsManager(db_models.Manager):
	pass