from rest_framework import generics, viewsets, serializers, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

# http://django-filter.readthedocs.io/en/stable/
import django_filters.rest_framework as rest_filter
import django_filters

from blog.shortcuts import get_current_blog
from accounts import models as account_models

from ..serializers import users
from .. import permissions


class UserFilter(rest_filter.FilterSet):

	class Meta:
		model = account_models.User
		fields = '__all__'


class UsersViewSet(viewsets.ModelViewSet):
	lookup_field = 'pk'
	queryset = account_models.User.objects.all()
	permission_classes = (permissions.SuperUserPermission,)
	filter_backends = (rest_filter.DjangoFilterBackend,)
	filter_class = UserFilter

	def get_serializer_class(self):
		return {
			'list': users.UserListSerializer,
			'retrieve': users.UserListSerializer,
			'update': users.UserListSerializer,
			'partial_update': users.UserListSerializer,
			'create': users.UserListSerializer,
			'metadata': users.UserListSerializer,
		}[self.action]
		