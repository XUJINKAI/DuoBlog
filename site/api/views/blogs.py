from rest_framework import generics, viewsets, serializers, permissions, status

from blog.models import Blog as BlogModel
from ..serializers.blogs import BlogListSerializer, BlogDetailSerializer
from ..permissions import BlogPermission


class BlogViewSet(viewsets.ModelViewSet):
	queryset = BlogModel.objects.all()
	permission_classes = (BlogPermission,)

	def get_serializer_class(self):
		return {
			'list': BlogListSerializer,
			'retrieve': BlogDetailSerializer,
			'update': BlogDetailSerializer,
			'partial_update': BlogDetailSerializer,
			'create': BlogDetailSerializer,
			'metadata': BlogListSerializer,
		}[self.action]