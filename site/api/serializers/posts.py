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


class PostViewSerializer(serializers.HyperlinkedModelSerializer):
	# author = PostAuthorSerializer(read_only=True)
	api_url = serializers.HyperlinkedIdentityField(view_name='api:post-detail', lookup_field='slug', read_only=True)
	html_url = serializers.HyperlinkedIdentityField(view_name='posts_detail', lookup_field='slug', read_only=True)
	tags = TagListSerializerField(format_string=True)

	class Meta:
		model = blog_models.Post
		fields = (
			'slug', 'api_url', 'html_url', \
			'create_time', 'last_modified_time', \
			'views_count', 'modified_count', \
			'tags', 'comments', 'sticky', 'status', \
			'title', 'content_type', 'content', \
			)
		read_only_fields = (
			'slug', 'api_url', 'html_url', \
			'create_time', 'last_modified_time', \
			'views_count', 'modified_count', \
			)



class PostListSerializer(PostViewSerializer):
	class Meta(PostViewSerializer.Meta):
		extra_kwargs = {'content': {'write_only': True}}

class PostDetailSerializer(PostViewSerializer):
	class Meta(PostViewSerializer.Meta):
		pass



class TagListSerializer(serializers.ModelSerializer):

    def from_native(self, data):
        if type(data) is not list:
            raise ParseError("expected a list of data")     
        return data
    
    def to_native(self, obj):
        if type(obj) is not list:
            return [tag.name for tag in obj.all()]
        return obj



class PostCreateSerializer(TaggitSerializer, serializers.ModelSerializer):
	tags = TagListSerializerField()

	class Meta:
		model = blog_models.Post
		fields = (
			'slug', 'title', 'content', 'content_type', \
			'status', 'tags', 'comments', 'sticky', \
			)

class PostUpdateSerializer(TaggitSerializer, serializers.ModelSerializer):
	tags = TagListSerializerField()

	class Meta:
		model = blog_models.Post
		fields = (
			'slug', 'title', 'content', 'content_type', \
			'status', 'tags', 'comments', 'sticky', \
			)