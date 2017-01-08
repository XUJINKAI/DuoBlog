from django.conf.urls import url
from . import views

app_name = 'manage'

urlpatterns = [
	url(r'^$', views.dashboard_view, name='index'),
	url(r'^dashboard$', views.dashboard_view, name='dashboard'),
	url(r'^posts$', views.posts_view, name='posts'),
	url(r'^posts/create/$', views.manage_view, {'page': 'post_create'}, name='post_create'),
	url(r'^pages$', views.pages_view, name='pages'),
	url(r'^comments$', views.comments_view, name='comments'),
	url(r'^blogs/$', views.blogs_view, name='blogs'),
	url(r'^blogs/(?P<site_pk>\d*)/$', views.blogs_view, name='blogs'),
	url(r'^blogs/(?P<site_pk>\d*)/delete/$', views.blogs_delete_view, name='blog_delete'),
	url(r'^blogs/create/$', views.blogs_create_view, name='blog_create'),
	url(r'^about/$', views.manage_view, {'page': 'about'}, name='about'),
	url(r'^import_jekyll/$', views.manage_view, {'page': 'import_jekyll'}, name='import_jekyll'),
	url(r'^export_jekyll/$', views.manage_view, {'page': 'export_jekyll'}, name='export_jekyll'),
]
