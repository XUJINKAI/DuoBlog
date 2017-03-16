from rest_framework import permissions
from django.conf import settings
from blog.shortcuts import get_current_blog


def general_permission(request):
	if settings.DEBUG and settings.DEBUG_API:
		return True
	if request.user.is_superuser:
		return True
	return False


class SuperUserPermission(permissions.BasePermission):

	def has_permission(self, request, view):
		return general_permission(request)

	def has_object_permission(self, request, view, obj):
		return general_permission(request)


class PostPermission(permissions.BasePermission):

	def has_permission(self, request, view):
		guest_perm = 'manage' not in request.GET
		return guest_perm \
			or general_permission(request)

	def has_object_permission(self, request, view, obj):
		guest_perm = 'manage' not in request.GET
		domain_match = request.META['HTTP_HOST'] == obj.blog.domain
		safe_method = request.method in permissions.SAFE_METHODS
		return guest_perm and domain_match and obj.is_public and safe_method \
			or general_permission(request)