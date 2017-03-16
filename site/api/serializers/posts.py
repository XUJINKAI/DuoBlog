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
	comments = serializers.BooleanField(source='comment_enable')

	class Meta:
		model = blog_models.Post
		fields = (
			'pk', 'slug', 'api_url', \
			'create_time', 'last_modified_time', \
			'views_count', 'modified_count', \
			'comments', 'status', \
			'title', 'content_type', 'abstract', \
			)


class PostDetailSerializer(serializers.ModelSerializer):
	api_url = serializers.HyperlinkedIdentityField(view_name='api:post-detail', lookup_field='pk', read_only=True)
	html_url = serializers.CharField(source='absolute_url')
	blog = serializers.IntegerField(source='blog.pk', required=False, read_only=True)
	comments = serializers.BooleanField(source='comment_enable')

	class Meta:
		model = blog_models.Post
		fields = (
			'pk', 'blog', 'slug', 'api_url', 'html_url', \
			'create_time', 'last_modified_time', \
			'views_count', 'modified_count', \
			'comments', 'deleted', 'status', \
			'title', 'content_type', 'content', 'rendered_html', \
			)



# create-update

class PostCreateSerializer(serializers.ModelSerializer):
	blog = serializers.IntegerField(source='blog.pk', required=False)
	comments = serializers.BooleanField(source='comment_enable', required=False, default=True)

	class Meta:
		model = blog_models.Post
		fields = (
			'pk', 'blog', 'slug', 'title', 'content', 'content_type', 'rendered_html', \
			'status', 'comments', 'tags', \
			)

	def create(self, validated_data):
		return super().create(validated_data)


class PostUpdateSerializer(PostCreateSerializer):
	class Meta(PostCreateSerializer.Meta):
		pass

	def update(self, instance, validated_data):
		if 'blog' in validated_data.keys():
			pk = validated_data['blog']['pk']
			blog = blog_models.Blog.objects.get(pk=pk)
			setattr(instance, 'blog', blog)
			del validated_data['blog']
		return super().update(instance, validated_data)