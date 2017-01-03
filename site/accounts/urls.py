from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index_view, name='accounts_index'),
	url(r'^login', views.login_view, name='accounts_login'),
	url(r'^signup', views.signup_view, name='accounts_login'),
	url(r'^createsuperuser', views.createsuperuser_view, name='accounts_createsuperuser'),
]
