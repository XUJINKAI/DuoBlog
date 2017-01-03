from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from . import models

# Create your views here.
def t(path):
	return 'themes/default/' + path


def index_view(request):
	return render(request, t('index.html'))


def post_detail(request):
	return render(request, t('posts/detail.html'))


@user_passes_test(lambda u:u.is_superuser)
def manage_blog(request):
	if not models.BlogSetting.is_setup():
		return HttpResponseRedirect(reverse('blog_setup')) 
	return render(request, 'manage/index.html')


@user_passes_test(lambda u:u.is_superuser)
def manage_blog_setup(request):
	if models.BlogSetting.is_setup():
		return HttpResponseRedirect(reverse('blog_manage'))
	return render(request, 'manage/setup.html')