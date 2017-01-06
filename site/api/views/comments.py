from rest_framework import viewsets, serializers, permissions
from blog import models as blog_models
from django.contrib.sites.models import Site


class CommentListSerializer(serializers.HyperlinkedModelSerializer):
	api_url = serializers.HyperlinkedIdentityField(view_name='api:blog-detail', read_only=True)
	site_id = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all())
	site_name = serializers.SerializerMethodField()
	site_domain = serializers.SerializerMethodField()

	class Meta:
		model = blog_models.Blog
		fields = ('api_url', 'site_id', 'site_name', 'site_domain', \
			'name', 'desc', 'navs', 'theme', \
			'new_post_content_type', 'posts_url_prefix', 'pages_url_prefix', \
			'google_analytics_id', 'disqus_id', \
			'rss', 'sitemap')

	def get_site_name(self, obj):
		return obj.site.name

	def get_site_domain(self, obj):
		return obj.site.domain


class CommentViewSet(viewsets.ModelViewSet):
	queryset = blog_models.Blog.objects.all()
	serializer_class = CommentListSerializer