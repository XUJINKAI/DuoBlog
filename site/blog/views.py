from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from . import models

# Create your views here.
_CURRENT_SITE = ''
_SITES_CACHE = None

def _load_sites_cache(request):
	global _CURRENT_SITE, _SITES_CACHE
	# //TODO
	# if not _SITES_CACHE:
	sites = Site.objects.all()
	for site in sites:
		if not hasattr(site, 'blog'):
			models.Blog.create(site=site).save()
	_SITES_CACHE = sites
	try:
		_CURRENT_SITE = get_current_site(request)
	except:
		raise Http404

def _t(request, path):
	global _CURRENT_SITE, _SITES_CACHE
	_load_sites_cache(request)
	return 'themes/' + _CURRENT_SITE.blog.theme + '/' + path

def _ctx(request, kwarg):
	global _CURRENT_SITE, _SITES_CACHE
	_load_sites_cache(request)
	ctx = {
		'blog': _CURRENT_SITE.blog,
	}
	return ctx


def blog_index(request):
	ctx = {}
	return render(request, _t(request, 'index.html'), _ctx(request, ctx))

def posts_list(request):
	ctx = {}
	return render(request, _t(request, 'posts_list.html'), _ctx(request, ctx))

def posts_detail(request, slug):
	ctx = {}
	return render(request, _t(request, 'posts_detail.html'), _ctx(request, ctx))