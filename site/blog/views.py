from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import user_passes_test
from . import models

# Create your views here.
def t(path):
	return 'themes/default/' + path


def blog_index(request):
	return render(request, t('index.html'))

def posts_list(request):
	return render(request, t('posts/detail.html'))

def posts_detail(request):
	return render(request, t('posts/detail.html'))


@user_passes_test(lambda u:u.is_superuser)
def manage_blog(request, url):
	# if not models.BlogSetting.is_setup():
	# 	return HttpResponseRedirect(reverse('blog_setup')) 
	menu = (
		# name, url, submenu
		('Dashboard', 'dashboard', None),
		('Posts', 'posts', None),
		('Pages', 'pages', None),
		('Tools', '#', (
			('Import Jekyll', 'import_jekyll', None),
			)
		),
	)
	ctx = {
		'menu': menu,
	}

	# max 3 level, the most quickest way
	for item in menu:
		if url == item[1]:
			return render(request, 'manage/'+ url +'.html', ctx)

		if item[2]:
			for item_sub in item[2]:
				if url == item_sub[1]:
					return render(request, 'manage/'+ url +'.html', ctx)

				if item_sub[2]:
					for item_sub_sub in item_sub[2]:
						if url == item_sub_sub[1]:
							return render(request, 'manage/'+ url +'.html', ctx)
	raise Http404