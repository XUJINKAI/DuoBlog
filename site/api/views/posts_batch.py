from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from blog import models as blog_models
from .. import permissions


class PostBatchView(APIView):
	lookup_field = 'pk'
	queryset = blog_models.Post.objects.all()
	permission_classes = (permissions.SuperUserPermission,)
	

	def post(self, request, *args, **kwargs):
		pass

	def delete(self, request, *args, **kwargs):
		delete_pks = request.POST.get('delete_pks', None)
		delete_pks = json.loads(delete_pks)
		for post in blog_models.Post.objects.filter(pk__in=delete_pks):
			post.delete()
		return Response({}, status=status.HTTP_204_NO_CONTENT)

	def put(self, request, *args, **kwargs):
		restore_pks = request.POST.get('restore_pks', None)
		if restore_pks:
			restore_pks = json.loads(restore_pks)
			for post in blog_models.Post.objects.filter(pk__in=restore_pks):
				post.restore()
			return Response({}, status=status.HTTP_202_ACCEPTED)