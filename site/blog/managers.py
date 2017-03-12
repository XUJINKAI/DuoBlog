from django.db import models as db_models
from .shortcuts import get_current_blog
from . import models as models


class PostManager(db_models.Manager):

	def blog_queryset(self, request, **kwargs):
		current_blog = get_current_blog(request)
		return self.filter(blog=current_blog, status='p')

	def api_list_queryset(self, request, **kwargs):
		'''
		parameter: blog(pk), status
		default: current, 'p'

		'''
		blog_pk = request.GET.get('blog', False)
		status = request.GET.get('status', 'p')

		if blog_pk:
			blog = models.Blog.objects.get(pk=blog_pk)
		else:
			blog = get_current_blog(request)

		return self.filter(blog=blog, status=status)

	def api_detail_queryset(self, request, **kwargs):
		return self


class TagsManager(db_models.Manager):
	pass

class CommentsManager(db_models.Manager):
	pass