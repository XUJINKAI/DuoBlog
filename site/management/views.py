from django.shortcuts import render
from django.views import generic
from django.views.generic.base import ContextMixin
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseBadRequest
from django.conf import settings
from django.views.decorators.http import require_http_methods

import json
from . import forms
from accounts import models as accounts_models
from blog import models
from blog.shortcuts import get_current_blog


def get_manage_context():
	context = {}
	context['menu'] = (
		# name, url, submenu
		('Dashboard', reverse('manage:dashboard'), None),
		('Posts', reverse('manage:posts'), None),
		('Pages', reverse('manage:pages'), None),
		('Comments', reverse('manage:comments'), None),
		('Blogs', reverse('manage:blogs'), None),
		('Tools', None, (
			('Import Jekyll', reverse('manage:import_jekyll'), None),
			('Export Jekyll', reverse('manage:export_jekyll'), None),
			),
		),
		('About', reverse('manage:about'), None),
	)
	context['blogs'] = models.Blog.objects.all()
	return context


class ManageContextMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		ctx = get_manage_context()
		context['menu'] = ctx['menu']
		context['blogs'] = ctx['blogs']
		return context


# general page show method
def manage_view(request, page):
	return render(request, 'manage/'+page+'.html', get_manage_context())


def dashboard_view(request):
	context = get_manage_context()
	infos = []
	# check blogs
	blogs = models.Blog.objects.all()
	if not blogs:
		infos.append({
			'msg': 'No blog exists. <a href="%s">Create</a>' % (reverse('manage:blogs'))
			})
	context['infos'] = infos
	return render(request, 'manage/dashboard.html', context)


class PostsView(ManageContextMixin, generic.TemplateView):
	template_name = 'manage/posts.html'

posts_view = PostsView.as_view()



# pages

class PagesView(ManageContextMixin, generic.TemplateView):
	template_name = 'manage/pages.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pages'] = models.Page.objects.all()
		return context

pages_view = PagesView.as_view()


class PagesEditView(ManageContextMixin, generic.TemplateView):
	template_name = 'manage/pages_edit.html'

	def get(self, request, page_pk=None):
		if page_pk:
			page = models.Page.objects.get(pk=page_pk)
			arr = page.url.split('/', 1)
			if len(arr) > 1:
				url_prefix, url_post = arr
			else:
				url_prefix, url_post = arr[0], '/'
			context = {
				'url_prefix': url_prefix,
				'url_post': url_post,
				'page': page,
			}
			return super().get(self, request, page_pk, **context)
		else:
			return super().get(self, request)

	def post(self, request, page_pk=None):
		if page_pk:
			page = models.Page.objects.get(pk=page_pk)
			form = forms.PageForm(request.POST, instance=page)
		else:
			form = forms.PageForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('manage:pages'))
		else:
			return HttpResponseBadRequest('form invalid')

	def delete(self, request, page_pk):
		page = models.Page.objects.get(pk=page_pk)
		page.delete()
		

pages_edit_view = PagesEditView.as_view()


# comment

class CommentsView(ManageContextMixin, generic.TemplateView):
	template_name = 'manage/comments.html'

comments_view = CommentsView.as_view()


# blogs opt
def blogs_view(request, blog_pk=None):
	if blog_pk:
		blog = models.Blog.objects.get(pk=blog_pk)
	else:
		blog = models.Blog.objects.first()
	if not blog:
		blog = models.Blog.create_new()
		return HttpResponseRedirect(reverse('manage:blogs', args=[blog.id]))
	context = get_manage_context()

	if request.method == 'POST':
		form = forms.BlogForm(request.POST, instance=blog)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('manage:blogs', args=[blog.id]))
	else:
		form = forms.BlogForm(instance=blog)

	context['form'] = form
	context['blog'] = blog
	context['blog_pk'] = blog.id
	context['blog_posts'] = models.Post.objects.filter(blog=blog).count()
	return render(request, 'manage/blogs.html', context)

@require_http_methods(['POST'])
def blogs_create_view(request):
	blog = models.Blog.create_new()
	return HttpResponseRedirect(reverse('manage:blogs', args=[blog.id]))

@require_http_methods(['POST'])
def blogs_delete_view(request, blog_pk):
	blog = models.Blog.objects.get(pk=blog_pk)
	blog.delete()
	return HttpResponseRedirect(reverse('manage:blogs'))

@require_http_methods(['POST'])
def blogs_navs_view(request, blog_pk):
	blog = models.Blog.objects.get(pk=blog_pk)
	blog.navs = request.POST.get('navs_json', '')
	blog.save()
	return HttpResponseRedirect(reverse('manage:blogs'))
