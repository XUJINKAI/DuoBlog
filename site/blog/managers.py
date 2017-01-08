from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from .shortcuts import get_current_blog


class PostManager(models.Manager):
	
	def accessible_queryset(self, request, **kwargs):
		'''
		return queryset by blog, user
		'''
		all_blogs = kwargs.get('all_blogs', False)
		queryset = self.all()

		# by blog
		if not all_blogs:
			current_blog = get_current_blog(request)
			queryset = queryset.filter(blog=current_blog)

		# by user
		if not request.user.is_superuser:
			queryset = queryset.filter(status='d')

		return queryset