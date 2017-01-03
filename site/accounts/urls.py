from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index_view, name='account_index'),
	url(r'^login', views.login_view, name='account_login'),
	url(r'^createsuperuser', views.createsuperuser_view, name='account_createsuperuser'),
]
