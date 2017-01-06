from django.conf.urls import url, include
from django.contrib.flatpages import views as flat_views
from . import views


urlpatterns = [
	url(r'^$', views.blog_index, name='index'),
	# posts/, posts/tags=a,b,c&order_by=name
	url(r'^posts/$', views.posts_list, name='posts_list'),
	url(r'^posts/(?P<slug>(?!/).*)/$', views.posts_detail, name='posts_detail'),
	# about/, pages/...
	url(r'^about/$', flat_views.flatpage, {'url': '/about/'}, name='about'),
	url(r'^(?=pages/)(?P<url>.*/)$', flat_views.flatpage, name='pages'),
]
