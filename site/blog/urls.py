from django.conf.urls import url, include
from . import views


urlpatterns = [
	url(r'^$', views.blog_index, name='index'),
    # url(r'^favicon\.ico$', views.favicon, name='favicon'),
	# posts/, posts/tags=a,b,c&order_by=name
	url(r'^posts/$', views.posts_list, name='posts_list'),
	url(r'^posts/(?P<slug>(?!/).*)/$', views.posts_detail, name='posts_detail'),
	# custom pages, for theme self
	url(r'^my/(?P<page>(?!/).*)/$', views.my_page, name='my_page'),
	# about/..., pages/...
	url(r'^(?=pages/|about/)(?P<url>.*)/$', views.page_view, name='pages'),
]
