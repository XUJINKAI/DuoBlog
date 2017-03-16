from rest_framework import generics, viewsets, serializers, permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

# http://django-filter.readthedocs.io/en/stable/
import django_filters.rest_framework as rest_filter
import django_filters

from blog import models as blog_models
from blog.shortcuts import get_current_blog
from accounts import models as account_models

from ..serializers.posts import PostListSerializer, PostCreateSerializer, \
					PostDetailSerializer, PostUpdateSerializer
from ..filters import MBooleanFilter
from ..permissions import PostPermission


class PostFilter(rest_filter.FilterSet):
	author = django_filters.CharFilter(name='author__username')
	content_type = MBooleanFilter(name='content_type')
	comments = MBooleanFilter(name='comment_enable')
	# admin only
	blog = django_filters.NumberFilter(name='blog__pk')
	status = MBooleanFilter(name='status')
	deleted = MBooleanFilter(name='deleted')

	class Meta:
		model = blog_models.Post
		fields = ['blog', 'status', 'deleted', 'slug', 'author', 'content_type', 'comments']


class PostViewSet(viewsets.ModelViewSet):
	lookup_field = 'pk'
	queryset = blog_models.Post.objects.all()
	permission_classes = (PostPermission,)
	filter_backends = (rest_filter.DjangoFilterBackend,)
	filter_class = PostFilter

	def get_serializer_class(self):
		return {
			'list': PostListSerializer,
			'retrieve': PostDetailSerializer,
			'update': PostUpdateSerializer,
			'partial_update': PostUpdateSerializer,
			'create': PostCreateSerializer,
			'metadata': PostListSerializer,
		}[self.action]

	def get_queryset(self):
		func_name = {
			'list': 'api_list_queryset',
			'retrieve': 'api_detail_queryset',
			'update': 'api_detail_queryset',
			'partial_update': 'api_detail_queryset',
			'destroy': 'api_detail_queryset',
		}[self.action]
		return getattr(blog_models.Post.objects, func_name)(self.request)
		

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
		serializer.save(author=self.request.user, blog=blog)
