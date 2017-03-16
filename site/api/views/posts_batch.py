from rest_framework.views import APIView
from rest_framework.response import Response
import json

class PostBatchViewSet(APIView):

	

	def delete(self, request, *args, **kwargs):
		delete_pks = request.POST.get('delete_pks', None)
		delete_pks = json.loads(delete_pks)
		blog_models.Post.objects.filter(pk__in=delete_pks).delete()
		return Response(status=status.HTTP_204_NO_CONTENT)