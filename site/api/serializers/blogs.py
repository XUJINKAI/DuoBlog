from rest_framework import serializers

from blog.models import Blog as BlogModel


class BlogListSerializer(serializers.HyperlinkedModelSerializer):
	api_url = serializers.HyperlinkedIdentityField(view_name='api:blog-detail', lookup_field='pk', read_only=True)

	class Meta:
		model = BlogModel
		fields = ('pk', 'api_url', 'name', 'domain', 'absolute_url', \
			'post_count', 'draft_count', 'trash_count', 'comment_count')


class BlogDetailSerializer(serializers.HyperlinkedModelSerializer):
	api_url = serializers.HyperlinkedIdentityField(view_name='api:blog-detail', lookup_field='pk', read_only=True)

	class Meta:
		model = BlogModel
		fields = ('pk', 'api_url', 'name', 'domain', 'absolute_url', 'desc', \
			'navs', 'theme', 'rss', 'sitemap', \
			'comments', 'custom_comment_html', \
			'head_html', 'body_html', \
			'post_count', 'draft_count', 'trash_count', 'comment_count', \
			)


class BlogCreateSerializer(serializers.ModelSerializer):
	rss = serializers.BooleanField(default=True)
	sitemap = serializers.BooleanField(default=True)

	class Meta:
		model = BlogModel
		fields = ('pk', 'name', 'domain', 'absolute_url', 'desc', \
			'navs', 'theme', 'rss', 'sitemap', \
			'comments', 'custom_comment_html', \
			'head_html', 'body_html', \
			)