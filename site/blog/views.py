from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from . import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from taggit.models import Tag

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
	PAGE_SIZE = 5
	try:
		site = get_current_site(request)
		page = request.GET.get('page', 1)
		posts = models.Post.objects.accessible_queryset(request)
		paginator = Paginator(posts, PAGE_SIZE)
		tags = Tag.objects.all()
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
	except Site.DoesNotExist:
		if request.get_host().split(':')[0] in ['localhost', '127.0.0.1']:
			return HttpResponseRedirect(reverse('manage:index'))
		else:
			raise Site.DoesNotExist


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
	tags = request.GET.get('tags', '').split(',')
	tags = [x for x in tags if x]
	qs = models.Post.objects.accessible_queryset(request)
	if tags:
		for tag in tags:
			qs = qs.filter(tags__name=tag)
		posts = qs
		remain_tags = set(tag.name for post in posts for tag in post.tags.all() if tag.name not in tags)
	else:
		posts = None
		remain_tags = set(tag.name for post in qs for tag in post.tags.all() if tag.name not in tags)
	context = {
		'posts': posts,
		'select_tags': tags,
		'remain_tags': remain_tags,
	}
	return render_theme(request, 'posts_list.html', context)


def my_page(request, page):
	print(page)
	return render_theme(request, 'my_%s.html' % page)