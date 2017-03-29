from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse

class RootView(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		content = {
			'version': reverse('api:version', request=request),
			'session': reverse('api:session', request=request),
			'users': reverse('api:user-list', request=request),
			'blogs': reverse('api:blog-list', request=request),
			'posts': reverse('api:post-list', request=request),
			'posts-batch': reverse('api:posts-batch', request=request),
		}
		return Response(content)
