from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models

SITE_CACHE = {}

def get_current_blog(request):
	host = request.get_host()
	try:
		if host not in SITE_CACHE:
			SITE_CACHE[host] = models.Blog.objects.get(domain__iexact=host)
		return SITE_CACHE[host]
	except:
		return None

# @receiver(post_save, sender=models.Blog)
def clear_cache():
	print('[CLEAR CACHE] SITE_CACHE')
	SITE_CACHE = {}
