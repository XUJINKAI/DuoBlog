from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from . import models

# Create your views here.
def render_theme(request, page_name, ctx=None):
	site = get_current_site(request)
	blog = site.blog
	render_page = 'themes/default/' + page_name
	if not ctx:
		ctx = {}
	ctx['blog'] = blog
	return render(request, render_page, ctx)


def blog_index(request):
	try:
		site = get_current_site(request)
		return render_theme(request, 'index.html')
	except Site.DoesNotExist:
		if request.get_host() in ['localhost', '127.0.0.1']:
			return HttpResponseRedirect(reverse('manage:index'))
		else:
			raise Site.DoesNotExist

def posts_list(request):
	return render_theme(request, 'posts_list.html')

def posts_detail(request, slug):
	return render_theme(request, 'posts_detail.html')