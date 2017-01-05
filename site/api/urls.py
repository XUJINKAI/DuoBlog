from django.conf.urls import url, include
from rest_framework import routers
from . import views


app_name = 'api'


router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)


urlpatterns = [
	url(r'^', include(router.urls)),
	# url(r'^', include('rest_framework.urls')),
]