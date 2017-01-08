from rest_framework import generics, viewsets, serializers, permissions
from rest_framework.views import APIView
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
	content_type = MBooleanFilter(name='content_type')
	author = django_filters.CharFilter(name='author__username')
	public = MBooleanFilter(name='status')
	sticky = MBooleanFilter(name='sticky')
	comments = MBooleanFilter(name='comments')

	class Meta:
		model = blog_models.Post
		fields = ['slug', 'content_type', 'author', 'public', 'sticky', 'comments']


class PostViewSet(viewsets.ModelViewSet):
	lookup_field = 'slug'
	queryset = blog_models.Post.objects.all()
	permission_classes = (PostPermission,)
	filter_backends = (rest_filter.DjangoFilterBackend,)
	filter_class = PostFilter

	def get_serializer_class(self):
		# print(self.request.POST)
		return {
			'list': PostListSerializer,
			'retrieve': PostDetailSerializer,
			'create': PostCreateSerializer,
			'update': PostUpdateSerializer,
			'partial_update': PostUpdateSerializer,
			'metadata': PostCreateSerializer,
		}[self.action]

	def get_queryset(self):
		return blog_models.Post.objects.accessible_queryset(self.request)


	def create(self, request, *args, **kwargs):
		return super().create(request, *args, **kwargs)

	def perform_create(self, serializer):
		serializer.save(author=self.request.user, blog=get_current_blog(self.request))