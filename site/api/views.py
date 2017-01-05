from rest_framework import viewsets, serializers, permissions

# http://django-filter.readthedocs.io/en/stable/
import django_filters.rest_framework as rest_filter
import django_filters

from blog import models as blog_models
from accounts import models as account_models


class MBooleanFilter(django_filters.Filter):

	def filter(self, qs, value):
		if value in [None, '']:
			return qs
		else:
			lc_value = value.lower()
			if lc_value in ["true", '1']:
				value = True
			elif lc_value in ["false", '0']:
				value = False
			return qs.filter(**{self.name: value})
		return qs


# post

class PostAuthorSerializer(serializers.HyperlinkedModelSerializer):
	# api_url = serializers.HyperlinkedIdentityField(view_name='api:user-detail', read_only=True)
	# html_url = serializers.HyperlinkedIdentityField(view_name='blog:detail', read_only=True)

	class Meta:
		model = account_models.User
		fields = ('username')

class PostBaseSerializer(serializers.HyperlinkedModelSerializer):
	# author = PostAuthorSerializer(read_only=True)
	api_url = serializers.HyperlinkedIdentityField(view_name='api:post-detail', lookup_field='slug', read_only=True)
	html_url = serializers.HyperlinkedIdentityField(view_name='posts_detail', lookup_field='slug', read_only=True)

	class Meta:
		model = blog_models.Post
		fields = (
			'slug', 'api_url', 'html_url', \
			'create_time', 'last_modified_time', \
			'views_count', 'modified_count', \
			'visible', 'sticky', 'show_comment', \
			'title', 'content_type', 'content', \
			)
		read_only_fields = (
			'slug', 'api_url', 'html_url', \
			'create_time', 'last_modified_time', \
			'views_count', 'modified_count', \
			)

class PostListSerializer(PostBaseSerializer):
	class Meta(PostBaseSerializer.Meta):
		extra_kwargs = {'content': {'write_only': True}}

class PostDetailSerializer(PostBaseSerializer):
	class Meta(PostBaseSerializer.Meta):
		pass

class PostPermission(permissions.BasePermission):
	def has_permission(self, request, view):
		return True

	def has_object_permission(self, request, view, obj):
		# owner or public & safe
		return obj.author == request.user or \
			obj.visible == 'p' and request.method in permissions.SAFE_METHODS

class PostFilter(rest_filter.FilterSet):
	content_type = MBooleanFilter(name='content_type')
	author = django_filters.CharFilter(name='author__username')
	public = MBooleanFilter(name='visible')
	sticky = MBooleanFilter(name='sticky')
	comment = MBooleanFilter(name='show_comment')

	class Meta:
		model = blog_models.Post
		fields = ['slug', 'content_type', 'author', 'public', 'sticky', 'comment']

class PostViewSet(viewsets.ModelViewSet):
	lookup_field = 'slug'
	queryset = blog_models.Post.objects.all()
	serializer_class = PostListSerializer
	permission_classes = (PostPermission,)
	filter_backends = (rest_filter.DjangoFilterBackend,)
	filter_class = PostFilter

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

	def get_serializer_class(self):
		if self.action == 'list':
			return PostListSerializer
		elif self.action == 'retrieve':
			return PostDetailSerializer
		return self.serializer_class

	def get_queryset(self):
		if self.request.user.is_staff:
			return blog_models.Post.objects.all()
		else:
			return blog_models.Post.objects.filter(visible='p')