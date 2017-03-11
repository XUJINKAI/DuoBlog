from rest_framework import permissions
from django.conf import settings


class DEBUG_API_MIXIN:
	def has_permission(self, request, view):
		if settings.DEBUG_API:
			return True
		return super().has_permission(self, request, view)

	def has_object_permission(self, request, view, obj):
		print(1)
		if settings.DEBUG_API:
			return True
		return super().has_object_permission(self, request, view, obj)


class PostPermission(DEBUG_API_MIXIN, permissions.BasePermission):

	def has_permission(self, request, view):
		if request.user.is_superuser:
			return True

		over_perm = request.GET.get('blog', False) or request.GET.get('status', False)
		return not over_perm


	def has_object_permission(self, request, view, obj):
		print(2)
		if request.user.is_superuser:
			return True

		safe = request.method in permissions.SAFE_METHODS
		return obj.status == 'p' and safe


class BlogPermission(DEBUG_API_MIXIN, permissions.BasePermission):
	pass