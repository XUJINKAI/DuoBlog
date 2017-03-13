from rest_framework import generics, viewsets, serializers, permissions, status
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
import json


class PostFilter(rest_filter.FilterSet):
	blog = django_filters.NumberFilter(name='blog__pk')
	content_type = MBooleanFilter(name='content_type')
	author = django_filters.CharFilter(name='author__username')
	status = MBooleanFilter(name='status')
	sticky = MBooleanFilter(name='sticky')
	comments = MBooleanFilter(name='comments')

	class Meta:
		model = blog_models.Post
		fields = ['blog', 'slug', 'content_type', 'author', 'status', 'sticky', 'comments']


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
		serializer.save(author=self.request.user, blog=get_current_blog(self.request))


	def delete(self, request, *args, **kwargs):
		delete_slugs = request.POST.get('delete_slugs', None)
		if delete_slugs:
			delete_slugs = json.loads(delete_slugs)
			blog_models.Post.objects.filter(slug__in=delete_slugs).delete()
			return Response(status=status.HTTP_204_NO_CONTENT)
		else:
			return super().destroy(request, *args, **kwargs)