from rest_framework import permissions
from django.conf import settings
from blog.shortcuts import get_current_blog

class BasePermission(permissions.BasePermission):

	def has_permission(self, request, view):
		if settings.DEBUG and settings.DEBUG_API:
			return True
		if request.user.is_superuser:
			return True
		return False

	def has_object_permission(self, request, view, obj):
		if settings.DEBUG and settings.DEBUG_API:
			return True
		if request.user.is_superuser:
			return True
		return False



class BlogPermission(BasePermission):
	pass


class PostPermission(BasePermission):

	def has_permission(self, request, view):
		over_perm = request.GET.get('blog', False) or request.GET.get('status', False)
		return not over_perm \
			or super().has_permission(request, view)

	def has_object_permission(self, request, view, obj):
		domain_match = request.META['HTTP_HOST'] == obj.blog.domain
		safe = request.method in permissions.SAFE_METHODS
		return domain_match and obj.status == 'p' and safe \
			or super().has_object_permission(request, view, obj)