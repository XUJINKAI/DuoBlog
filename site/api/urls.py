from django.conf.urls import url, include
from rest_framework import routers
from .views.blogs import BlogViewSet
from .views.posts import PostViewSet
from .views.comments import CommentViewSet
from .views.img import img_view
from .views.session import SessionView


app_name = 'api'

router = routers.DefaultRouter()
router.register(r'blogs', BlogViewSet)
router.register(r'posts', PostViewSet)
# router.register(r'comments', CommentViewSet)


urlpatterns = [
	url(r'^', include(router.urls)),
	url(r'^session/', SessionView.as_view()),
	# session
	# users
	# blogs/<pk>/tags	GET
	# tags				GET
	# posts/<slug>/comments
	# comments
	url(r'^img/', img_view),
	# url(r'^', include('rest_framework.urls')),
]