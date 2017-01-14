from django.db import models
from .shortcuts import get_current_blog


class PostManager(models.Manager):
	
	def accessible_queryset(self, request, **kwargs):
		'''
		return queryset by blog, user
		'''
		all_blogs = kwargs.get('all_blogs', False)
		queryset = self.all()

		# filter by blog
		if not all_blogs:
			current_blog = get_current_blog(request)
			queryset = queryset.filter(blog=current_blog)

		# filter by user
		if not request.user.is_superuser:
			queryset = queryset.filter(status='p')

		return queryset