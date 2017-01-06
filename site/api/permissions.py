from rest_framework import permissions


class PostPermission(permissions.BasePermission):
	def has_permission(self, request, view):
		return True

	def has_object_permission(self, request, view, obj):
		# owner or public & safe
		return obj.author == request.user or \
			obj.status == 'p' and request.method in permissions.SAFE_METHODS


# class 