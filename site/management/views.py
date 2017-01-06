from django.shortcuts import render
from django.views import generic
from django.views.generic.base import ContextMixin
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.conf import settings

from django.contrib.sites.models import Site
from accounts import models as accounts_models
from blog import models
from . import forms


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
	context['sites'] = Site.objects.all()
	return context


class ManageContextMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		ctx = get_manage_context()
		context['menu'] = ctx['menu']
		context['sites'] = ctx['sites']
		return context


def manage_view(request, page):
	return render(request, 'manage/'+page+'.html', get_manage_context())


class DashboardView(ManageContextMixin, generic.TemplateView):
	template_name = 'manage/dashboard.html'

dashboard_view = DashboardView.as_view()


class PostsView(ManageContextMixin, generic.TemplateView):
	template_name = 'manage/posts.html'

posts_view = PostsView.as_view()


class PagesView(ManageContextMixin, generic.TemplateView):
	template_name = 'manage/pages.html'

pages_view = PagesView.as_view()


class CommentsView(ManageContextMixin, generic.TemplateView):
	template_name = 'manage/comments.html'

comments_view = CommentsView.as_view()


class BlogsView(ManageContextMixin, generic.TemplateView):
	template_name = 'manage/blogs.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = forms.BlogForm()
		return context

blogs_view = BlogsView.as_view()


class ProfileView(ManageContextMixin, generic.TemplateView):
	template_name = 'manage/profile.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = forms.UserForm(instance=self.request.user)
		return context

profile_view = ProfileView.as_view()
