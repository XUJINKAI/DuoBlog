from rest_framework import generics, viewsets, serializers, status

from blog.models import Blog as BlogModel
from ..serializers.blogs import BlogListSerializer, BlogDetailSerializer, BlogCreateSerializer
from .. import permissions


class BlogViewSet(viewsets.ModelViewSet):
	queryset = BlogModel.objects.all()
	permission_classes = (permissions.SuperUserPermission,)

	def get_serializer_class(self):
		return {
			'list': BlogListSerializer,
			'retrieve': BlogDetailSerializer,
			'update': BlogCreateSerializer,
			'partial_update': BlogCreateSerializer,
			'create': BlogCreateSerializer,
			'metadata': BlogListSerializer,
		}[self.action]