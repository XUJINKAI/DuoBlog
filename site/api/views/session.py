from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import logout, login, authenticate

class SessionView(APIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (AllowAny,)

	def request_status(self, request):
		if request.user.is_authenticated:
			content = {
				'login': True,
				'username': request.user.username,
			}
		else:
			content = {
				'login': False,
				'username': '',
			}
		return content

	def get(self, request):
		return Response(self.request_status(request))

	def post(self, request):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
		return Response(self.request_status(request))

	def delete(self, request):
		logout(request)
		return Response(self.request_status(request))