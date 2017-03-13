from django.conf.urls import url, include
from . import views


urlpatterns = [
	url(r'^$', views.blog_index, name='index'),
	url(r'^p/(?P<slug>(?!/).*)/$', views.post_show, name='posts_detail'),
	url(r'^posts/$', views.posts_list, name='posts_list'),
	url(r'^my/(?P<page>(?!/).*)/$', views.my_page, name='my_page'),
	url(r'^manage/$', views.manage_view, name='manage_index'),
]
