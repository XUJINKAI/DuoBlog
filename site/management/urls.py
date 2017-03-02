from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^note/$', views.note_view, name='manage_contents'),
	url(r'^$', views.dashboard_view, name='manage_index'),
	url(r'^dashboard/$', views.dashboard_view, name='manage_dashboard'),
	url(r'^posts/$', views.posts_view, name='manage_posts'),
	url(r'^posts/create/$', views.manage_view, {'page': 'posts_create'}, name='manage_post_create'),
	url(r'^pages/$', views.pages_view, name='manage_pages'),
	url(r'^pages/create/$', views.pages_edit_view, name='manage_page_edit'),
	url(r'^pages/edit/(?P<page_pk>\d+)/$', views.pages_edit_view, name='manage_page_edit'),
	url(r'^comments$', views.comments_view, name='manage_comments'),
	url(r'^blogs/$', views.blogs_view, name='manage_blogs'),
	url(r'^blogs/(?P<blog_pk>\d+)/$', views.blogs_view, name='manage_blogs'),
	url(r'^blogs/(?P<blog_pk>\d+)/delete/$', views.blogs_delete_view, name='manage_blog_delete'),
	url(r'^blogs/(?P<blog_pk>\d+)/navs$', views.blogs_navs_view, name='manage_blog_navs'),
	url(r'^blogs/create/$', views.blogs_create_view, name='manage_blog_create'),
	url(r'^about/$', views.manage_view, {'page': 'about'}, name='manage_about'),
	url(r'^import_jekyll/$', views.manage_view, {'page': 'import_jekyll'}, name='manage_import_jekyll'),
	url(r'^export_jekyll/$', views.manage_view, {'page': 'export_jekyll'}, name='manage_export_jekyll'),
]
