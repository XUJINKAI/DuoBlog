from django.shortcuts import render
from django.views import generic
from django.views.generic.base import ContextMixin
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.conf import settings
from django.views.decorators.http import require_http_methods

from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site

from accounts import models as accounts_models
from blog import models
from . import forms
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
	# context['sites'] = Site.objects.all()
	context['blogs'] = models.Blog.objects.all()
	return context


class ManageContextMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		ctx = get_manage_context()
		context['menu'] = ctx['menu']
		# context['sites'] = ctx['sites']
		context['blogs'] = ctx['blogs']
		return context


# general page show method
def manage_view(request, page):
	return render(request, 'manage/'+page+'.html', get_manage_context())


def dashboard_view(request):
	context = get_manage_context()
	infos = []
	# check sites
	sites = Site.objects.all()
	if not sites:
		infos.append({
			'msg': 'No sites exists. <a href="%s">Create</a>' % (reverse('manage:blogs'))
			})
	else:
		for site in Site.objects.all():
			blog = models.Blog.objects.filter(domain=site.domain).first()
			if not blog:
				infos.append({
					'msg': 'Site <strong>"%s"</strong> exists but no blog related. <strong><a href="%s">Click to see detail</a></strong>' \
						% (site.domain, reverse('manage:blogs', args=[site.id]))
					})
	context['infos'] = infos
	return render(request, 'manage/dashboard.html', context)


class PostsView(ManageContextMixin, generic.TemplateView):
	template_name = 'manage/posts.html'

posts_view = PostsView.as_view()


class PagesView(ManageContextMixin, generic.TemplateView):
	template_name = 'manage/pages.html'

pages_view = PagesView.as_view()


class CommentsView(ManageContextMixin, generic.TemplateView):
	template_name = 'manage/comments.html'

comments_view = CommentsView.as_view()


# blogs opt
def blogs_view(request, site_pk=None):
	if site_pk:
		site = Site.objects.get(pk=site_pk)
	else:
		site = Site.objects.first()
	if not site:
		blog = models.Blog.create_new()
		return HttpResponseRedirect(reverse('manage:blogs', args=[blog.site.id]))
	blog = models.Blog.objects.filter(domain=site.domain).first()
	if not blog:
		blog = models.Blog.get_or_create_by_site(site)
	context = get_manage_context()

	if request.method == 'POST':
		form = forms.BlogForm(request.POST, instance=blog)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('manage:blogs', args=[site.id]))
	else:
		form = forms.BlogForm(instance=blog)

	context['form'] = form
	context['blog'] = blog
	context['site_pk'] = site.id
	context['sites'] = Site.objects.all()
	return render(request, 'manage/blogs.html', context)

@require_http_methods(['POST'])
def blogs_create_view(request):
	blog = models.Blog.create_new()
	return HttpResponseRedirect(reverse('manage:blogs', args=[blog.site.id]))

@require_http_methods(['POST'])
def blogs_delete_view(request, site_pk):
	if site_pk:
		site = Site.objects.get(pk=site_pk)
	else:
		site = Site.objects.first()
	site.delete()
	return HttpResponseRedirect(reverse('manage:blogs'))
