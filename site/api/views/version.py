from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import os

from ..permissions import VersionPermission


class VersionView(APIView):
	permission_classes = (VersionPermission,)

	def get_version_obj(self):
		content = {
			'version': '0.0.0',
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
		if action == 'update':
			try:
				self.do_update()
				msg = 'updated'
			except OnWinException:
				msg = 'update error: running on windows'
			except Exception as e:
				msg = 'update error: %s' % e.strerror
		else:
			msg = 'no action'
		return Response({'msg': msg})

version_view = VersionView.as_view()


class OnWinException(Exception):
	pass