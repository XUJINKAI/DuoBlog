from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import forms
from django.conf import settings
import os
from django.utils.crypto import get_random_string



def get_random_id(length):
	return get_random_string(length=length, allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789')


def handle_uploaded_file(f):
	# //TODO
	url = os.path.join(settings.STATIC_URL, 'img', str(f))
	if not settings.DEBUG:
		raise Exception('//TODO why following not work?')
	# file_path = os.path.join(settings.BASE_DIR, url)
	file_path = settings.BASE_DIR + url
	with open(file_path, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	return url


def img_view(request):
	if request.method == 'POST':
		try:
			img_link = handle_uploaded_file(request.FILES['file'])
			return HttpResponse(img_link)
		except Exception as e:
			return HttpResponse('error|%s' % str(e))
	else:
		return HttpResponse('error|Not POST method')