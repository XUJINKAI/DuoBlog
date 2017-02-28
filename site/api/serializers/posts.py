from rest_framework import serializers
from accounts import models as account_models

from blog import models as blog_models

# from .tags import TagSerializerField
from taggit.utils import parse_tags
from .taggit import TagListSerializerField, TaggitSerializer


class PostAuthorSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = account_models.User
		fields = ('username', )



# view

class PostListSerializer(serializers.ModelSerializer):
	api_url = serializers.HyperlinkedIdentityField(view_name='api:post-detail', lookup_field='slug', read_only=True)
	html_url = serializers.HyperlinkedIdentityField(view_name='posts_detail', lookup_field='slug', read_only=True)
	tags = TagListSerializerField(format_string=True, read_only=True)

	class Meta:
		model = blog_models.Post
		fields = (
			'slug', 'api_url', 'html_url', \
			'create_time', 'last_modified_time', \
			'views_count', 'modified_count', \
			'tags', 'comments', 'sticky', 'status', \
			'title', 'content_type', \
			)


class PostDetailSerializer(serializers.ModelSerializer):
	api_url = serializers.HyperlinkedIdentityField(view_name='api:post-detail', lookup_field='slug', read_only=True)
	html_url = serializers.HyperlinkedIdentityField(view_name='posts_detail', lookup_field='slug', read_only=True)
	tags = TagListSerializerField(format_string=True, read_only=True)

	class Meta:
		model = blog_models.Post
		fields = (
			'slug', 'api_url', 'html_url', \
			'create_time', 'last_modified_time', \
			'views_count', 'modified_count', \
			'tags', 'comments', 'sticky', 'status', \
			'title', 'content_type', 'content', 'rendered_html', \
			)



# create-update

class PostCreateSerializer(TaggitSerializer, serializers.ModelSerializer):
	tags = TagListSerializerField()

	class Meta:
		model = blog_models.Post
		fields = (
			'slug', 'title', 'content', 'content_type', 'rendered_html', \
			'status', 'tags', 'comments', 'sticky', \
			)

class PostUpdateSerializer(PostCreateSerializer):
	class Meta(PostCreateSerializer.Meta):
		pass