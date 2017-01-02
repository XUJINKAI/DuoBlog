from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.
def t(path):
	return 'themes/default/' + path


def index_view(request):
	return render(request, t('index.html'))


def post_detail(request):
	return render(request, t('posts/detail.html'))


def manage_blog(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('account_login'))
	return render(request, 'manage/index.html')