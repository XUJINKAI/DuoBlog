from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from distutils.version import StrictVersion
import os

from ..permissions import VersionPermission


class VersionView(APIView):
	permission_classes = (VersionPermission,)

	def get_version_obj(self):
		content = {
			'version': str(StrictVersion('0.0.0')),
		}
		return content

	def get_update_sh(self):
		return os.path.join(os.path.dirname(settings.BASE_DIR), 'update.sh')

	def do_update(self):
		update_sh = self.get_update_sh()
		if os.name == 'nt':
			raise OnWinException
		import subprocess
		subprocess.call(['sh', update_sh])

	def get(self, request):
		content = self.get_version_obj()
		return Response(content)

	def post(self, request):
		action = request.data.get('action')
		msg = 'init'
		sta = status.HTTP_200_OK
		if action == 'update':
			try:
				self.do_update()
				msg = 'updated'
			except OnWinException:
				msg = 'update error: running on windows'
				sta = status.HTTP_500_INTERNAL_SERVER_ERROR
			except Exception as e:
				msg = 'update error: %s' % e.strerror
				sta = status.HTTP_500_INTERNAL_SERVER_ERROR
		else:
			msg = 'no action'
			sta = status.HTTP_400_BAD_REQUEST
		return Response({'msg': msg}, status=sta)

version_view = VersionView.as_view()


class OnWinException(Exception):
	pass