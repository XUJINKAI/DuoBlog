from django.conf.urls import url
from django.contrib.flatpages import views as flat_views
from . import views


urlpatterns = [
	url(r'^$', views.blog_index, name='blog_index'),
	# posts/, posts/tags=a,b,c&order_by=name
	url(r'^posts/$', views.posts_list, name='posts_list'),
	url(r'^posts/(?P<slug>(?!/).*)/$', views.posts_detail, name='posts_detail'),
	# about/, pages/...
	url(r'^about/$', flat_views.flatpage, {'url': '/about/'}, name='blog_about'),
	url(r'^(?=pages/)(?P<url>.*/)$', flat_views.flatpage),
	# manage/...
	url(r'^manage/$', views.manage_blog, {'url': 'dashboard'}, name='blog_manage'),
	url(r'^manage/(?P<url>(?!/).*)/$', views.manage_blog, name='blog_manage'),
]
