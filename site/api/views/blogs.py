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
			'update': BlogListSerializer,
			'partial_update': BlogListSerializer,
			'create': BlogListSerializer,
			'metadata': BlogListSerializer,
		}[self.action]