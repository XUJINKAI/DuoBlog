from django.conf.urls import url, include
from rest_framework import routers
from .views.posts import PostViewSet
from .views.tags import TagViewSet
from .views.comments import CommentViewSet


app_name = 'api'


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'tags', TagViewSet)
router.register(r'comments', CommentViewSet)


urlpatterns = [
	url(r'^', include(router.urls)),
	# url(r'^', include('rest_framework.urls')),
]