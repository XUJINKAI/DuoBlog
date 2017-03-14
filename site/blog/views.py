from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.exceptions import MultipleObjectsReturned
from django.conf import settings

import json
from collections import Counter

from . import models
from .shortcuts import get_current_blog
from .helpers import Paginator

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
	PAGE_SIZE = 10

	blog = get_current_blog(request)
	if not blog:
		return HttpResponseRedirect(reverse('manage_index'))
	queryset = models.Post.objects.blog_queryset(request)
	sticky_posts = queryset.filter(sticky=True)
	all_posts = queryset.filter(sticky=False)

	PAGE, MAX_PAGE, NEXT_PAGE, PREV_PAGE, START, END = Paginator(request.GET.get('page'), all_posts.count(), PAGE_SIZE)
	next_page_url = '?page=%d' % (NEXT_PAGE,) if NEXT_PAGE else False
	prev_page_url = '?page=%d' %(PREV_PAGE) if PREV_PAGE else False
	prev_page_url = '/' if PREV_PAGE == 1 else prev_page_url
	posts = all_posts[START : END]
	# tags = set(tag.name for post in queryset for tag in post.tags.all())
	tags = []
	context = {
		'sticky_posts': sticky_posts,
		'posts': posts,
		'tags': tags,
		'current_page': PAGE,
		'prev_page_url': prev_page_url,
		'next_page_url': next_page_url,
	}
	return render_theme(request, 'index.html', context)


def post_show(request, slug):
	post = models.Post.objects.blog_queryset(request).filter(slug=slug).first()
	if not post:
		raise Http404
	# tags_href_string = ', '.join(['<a href="%s?tags=%s">%s</a>' \
	# 		% (reverse('posts_list'), tag.name, tag.name) for tag in post.tags.all()])
	tags_href_string = ''
	post_comment = post.comment_enable
	blog_comment = post.blog.comments
	context = {
		'post': post,
		'tags_href_string': tags_href_string,
		'custom_comment': post_comment and blog_comment=='c',
		'anyone_comment': post_comment and blog_comment=='a',
		'login_comment': post_comment and blog_comment=='l',
	}
	if context['custom_comment']:
		context['custom_comment_html'] = post.blog.custom_comment_html
	return render_theme(request, 'post_default.html', context)


def posts_list(request):
	# search_tags = [x for x in request.GET.get('tags', '').split(',') if x]
	all_posts = models.Post.objects.blog_queryset(request)
	# if search_tags:
	# 	qs = all_posts
	# 	for tag in search_tags:
	# 		qs = qs.filter(tags__name=tag)
	# 	posts = qs
	# 	posts_tags = set(tag.name for post in posts for tag in post.tags.all())
	# else:
	# 	posts = all_posts[:100]
	# 	posts_tags = set(tag.name for post in all_posts for tag in post.tags.all())
	all_tags = []
	# for p in Counter(tag.name for post in all_posts for tag in post.tags.all()).most_common():
	# 	all_tags.append({
	# 		'name': p[0],
	# 		'count': p[1],
	# 		'selected': p[0] in search_tags,
	# 		'overlap': p[0] in posts_tags,
	# 		})
	context = {
		'posts': all_posts,
		'all_tags': all_tags,
	}
	return render_theme(request, 'posts_list.html', context)


def my_page(request, page):
	return render_theme(request, 'my_%s.html' % page)


# //TODO cache
def sitemap_txt(request):
	blog = get_current_blog(request)
	if not blog.sitemap:
		raise Http404
	url = blog.absolute_url + settings.POSTS_URL_FIELD + '/'
	posts = models.Post.objects.blog_queryset(request)
	txt = ''
	for post in posts:
		txt += url + post.slug + '\r\n'
	return HttpResponse(txt, content_type='text/plain')


# admin SPA
def manage_view(request):
	return render(request, 'manage/index.html')