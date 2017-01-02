from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index_view, name='index'),
	url(r'^posts/(?P<slug>(?!/).*)/', views.post_detail, name='post_detail'),
	url(r'^manage/', views.manage_blog, name='blog_manage'),
]
