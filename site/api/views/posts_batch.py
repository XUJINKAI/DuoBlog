from rest_framework.views import APIView
from rest_framework.response import Response
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
		blog_models.Post.objects.filter(pk__in=delete_pks).delete()
		return Response(status=status.HTTP_204_NO_CONTENT)