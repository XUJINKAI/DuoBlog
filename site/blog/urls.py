from django.conf.urls import url
from django.contrib.flatpages import views as flat_views
from . import views


urlpatterns = [
	url(r'^$', views.index_view, name='index'),
	url(r'^posts/tags/$', views.post_detail, name='post_tags_filter'),
	url(r'^posts/(?P<slug>(?!/).*)/$', views.post_detail, name='post_detail'),
	url(r'^posts/(?P<slug>(?!/).*)/edit/$', views.post_detail, name='post_detail'),
	url(r'^manage/setup', views.manage_blog_setup, name='blog_setup'),
	url(r'^manage/', views.manage_blog, name='blog_manage'),
	url(r'^about/$', flat_views.flatpage, {'url': '/about/'}, name='blog_about'),
	url(r'^(?=pages/)(?P<url>.*/)$', flat_views.flatpage),
]
