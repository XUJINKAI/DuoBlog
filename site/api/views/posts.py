from rest_framework import generics, viewsets, serializers, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

# http://django-filter.readthedocs.io/en/stable/
import django_filters.rest_framework as rest_filter
import django_filters

from blog import models as blog_models
from blog.shortcuts import get_current_blog

from ..serializers import posts
from .. import permissions
from ..filters import MBooleanFilter


class PostFilter(rest_filter.FilterSet):
	blog = django_filters.NumberFilter(name='blog__pk')
	content_type = MBooleanFilter(name='content_type')
	comments = MBooleanFilter(name='comment_enable')
	status = MBooleanFilter(name='status')
	deleted = MBooleanFilter(name='deleted')

	class Meta:
		model = blog_models.Post
		fields = ['blog', 'slug', 'content_type', 'comments', 'status', 'deleted']


class PostViewSet(viewsets.ModelViewSet):
	lookup_field = 'pk'
	queryset = blog_models.Post.objects.all()
	permission_classes = (permissions.SuperUserPermission,)
	filter_backends = (rest_filter.DjangoFilterBackend,)
	filter_class = PostFilter

	def get_serializer_class(self):
		return {
			'list': posts.PostListSerializer,
			'retrieve': posts.PostDetailSerializer,
			'update': posts.PostUpdateSerializer,
			'partial_update': posts.PostUpdateSerializer,
			'create': posts.PostCreateSerializer,
			'metadata': posts.PostListSerializer,
		}[self.action]
		
		
	def create(self, request, *args, **kwargs):
		if not get_current_blog(self.request):
			return Response({
				'error': 'your request domain not found'
				}, status=status.HTTP_403_FORBIDDEN)
		return super().create(request, *args, **kwargs)

	def perform_create(self, serializer):
		blog_pk = self.request.POST.get('blog', False)
		if blog_pk:
			blog = blog_models.Blog.objects.get(pk=int(blog_pk))
		else:
			blog = get_current_blog(self.request)
		serializer.save(blog=blog)