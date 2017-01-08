from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site

from . import models


def get_current_blog(request):
	try:
		site = get_current_site(request)
	except Site.DoesNotExist:
		return None
	return site.blog