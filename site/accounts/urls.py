from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='account_index'),
	url(r'^login', views.login, name='account_login'),
	url(r'^createsuperuser', views.createsuperuser, name='account_createsuperuser'),
]
