from rest_framework import serializers

from blog.models import Blog as BlogModel


class BlogListSerializer(serializers.HyperlinkedModelSerializer):
	api_url = serializers.HyperlinkedIdentityField(view_name='api:blog-detail', lookup_field='pk', read_only=True)
	url = serializers.CharField(source='domain')

	class Meta:
		model = BlogModel
		fields = ('pk', 'api_url', 'name', 'url', \
			'post_count', 'draft_count', 'trash_count', 'comment_count')


class BlogDetailSerializer(serializers.HyperlinkedModelSerializer):
	api_url = serializers.HyperlinkedIdentityField(view_name='api:blog-detail', lookup_field='pk', read_only=True)
	url = serializers.CharField(source='domain')

	class Meta:
		model = BlogModel
		fields = ('pk', 'api_url', 'name', 'url', 'desc', \
			'post_count', 'draft_count', 'trash_count', 'comment_count', \
			'head_html', 'body_html', 'custom_comment_html')