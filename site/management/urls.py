from django.conf.urls import url
from . import views

app_name = 'manage'

urlpatterns = [
	url(r'^$', views.dashboard_view, name='index'),
	url(r'^dashboard$', views.dashboard_view, name='dashboard'),
	url(r'^posts$', views.posts_view, name='posts'),
	url(r'^pages$', views.pages_view, name='pages'),
	url(r'^comments$', views.comments_view, name='comments'),
	url(r'^blogs/', views.blogs_view, name='blogs'),
	url(r'^about/$', views.manage_view, {'page': 'about'}, name='about'),
	url(r'^profile/$', views.profile_view, name='profile'),
	url(r'^import_jekyll/$', views.manage_view, {'page': 'import_jekyll'}, name='import_jekyll'),
	url(r'^export_jekyll/$', views.manage_view, {'page': 'export_jekyll'}, name='export_jekyll'),
]
