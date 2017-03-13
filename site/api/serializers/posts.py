from rest_framework import serializers
from accounts import models as account_models

from blog import models as blog_models


class PostAuthorSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = account_models.User
		fields = ('username', )



# view

class PostListSerializer(serializers.ModelSerializer):
	api_url = serializers.HyperlinkedIdentityField(view_name='api:post-detail', lookup_field='pk', read_only=True)
	html_url = serializers.HyperlinkedIdentityField(view_name='posts_detail', lookup_field='slug', read_only=True)

	class Meta:
		model = blog_models.Post
		fields = (
			'pk', 'slug', 'api_url', 'html_url', \
			'create_time', 'last_modified_time', \
			'views_count', 'modified_count', \
			'comments', 'sticky', 'status', \
			'title', 'content_type', 'abstract', \
			)


class PostDetailSerializer(serializers.ModelSerializer):
	api_url = serializers.HyperlinkedIdentityField(view_name='api:post-detail', lookup_field='pk', read_only=True)
	html_url = serializers.HyperlinkedIdentityField(view_name='posts_detail', lookup_field='slug', read_only=True)

	class Meta:
		model = blog_models.Post
		fields = (
			'pk', 'slug', 'api_url', 'html_url', \
			'create_time', 'last_modified_time', \
			'views_count', 'modified_count', \
			'comments', 'sticky', 'status', \
			'title', 'content_type', 'content', 'rendered_html', \
			)



# create-update

class PostCreateSerializer(serializers.ModelSerializer):

	class Meta:
		model = blog_models.Post
		fields = (
			'pk', 'slug', 'title', 'content', 'content_type', 'rendered_html', \
			'status', 'comments', 'sticky', \
			)

class PostUpdateSerializer(PostCreateSerializer):
	class Meta(PostCreateSerializer.Meta):
		pass