from django.db import models
from .shortcuts import get_current_blog


class PostManager(models.Manager):

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
			blog = models.Blog.get(pk=blog_pk)
		else:
			blog = get_current_blog(request)

		return self.filter(blog=blog, status=status)


class TagsManager(models.Manager):
	pass

class CommentsManager(models.Manager):
	pass