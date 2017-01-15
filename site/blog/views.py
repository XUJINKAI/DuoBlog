from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from taggit.models import Tag
from django.core.exceptions import MultipleObjectsReturned

import json
from collections import Counter

from . import models
from .shortcuts import get_current_blog

# Create your views here.
def render_theme(request, page_name, ctx=None):
	blog = get_current_blog(request)
	render_page = 'themes/%s/%s' % (blog.theme, page_name)
	if not ctx:
		ctx = {}
	ctx['blog'] = blog
	try:
		if blog.navs is '':
			ctx['navs'] = []
		else:
			ctx['navs'] = json.loads(blog.navs)
	except:
		ctx['navs'] = []
	return render(request, render_page, ctx)


def blog_index(request):
	PAGE_SIZE = 5
	blog = get_current_blog(request)
	if not blog:
		return HttpResponseRedirect(reverse('manage:index'))
	page = request.GET.get('page', 1)
	posts = models.Post.objects.accessible_queryset(request)
	paginator = Paginator(posts, PAGE_SIZE)
	tags = set(tag.name for post in posts for tag in post.tags.all())
	try:
		pagi_posts = paginator.page(page)
	except PageNotAnInteger:
		pagi_posts = paginator.page(1)
	except EmptyPage:
		pagi_posts = paginator.page(paginator.num_pages)
	context = {
		'posts': pagi_posts,
		'tags': tags,
	}
	return render_theme(request, 'index.html', context)


def posts_detail(request, slug):
	post = models.Post.objects.accessible_queryset(request).filter(slug=slug).first()
	if not post:
		raise Http404
	tags_href_string = ', '.join(['<a href="%s?tags=%s">%s</a>' \
			% (reverse('posts_list'), tag.name, tag.name) for tag in post.tags.all()])
	context = {
		'post': post,
		'tags_href_string': tags_href_string,
	}
	return render_theme(request, 'posts_detail.html', context)


def posts_list(request):
	search_tags = [x for x in request.GET.get('tags', '').split(',') if x]
	all_posts = models.Post.objects.accessible_queryset(request)
	if search_tags:
		qs = all_posts
		for tag in search_tags:
			qs = qs.filter(tags__name=tag)
		posts = qs
		posts_tags = set(tag.name for post in posts for tag in post.tags.all())
	else:
		posts = all_posts[:100]
		posts_tags = set(tag.name for post in all_posts for tag in post.tags.all())
	all_tags = []
	for p in Counter(tag.name for post in all_posts for tag in post.tags.all()).most_common():
		all_tags.append({
			'name': p[0],
			'count': p[1],
			'selected': p[0] in search_tags,
			'overlap': p[0] in posts_tags,
			})
	context = {
		'posts': posts,
		'all_tags': all_tags,
	}
	return render_theme(request, 'posts_list.html', context)


def my_page(request, page):
	return render_theme(request, 'my_%s.html' % page)


# flatpage
def page_view(request, url):
	blog = get_current_blog(request)
	try:
		page = models.Page.objects.get(blog=blog, url=url.strip('/'))
	except MultipleObjectsReturned:
		raise
	except:
		raise Http404
	return render_theme(request, 'pages_template.html', {'page': page})