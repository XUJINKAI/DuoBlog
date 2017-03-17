from django.conf.urls import url, include
from rest_framework import routers

from .views.root import RootView
from .views.session import SessionView
from .views.users import UsersViewSet
from .views.blogs import BlogViewSet
from .views.posts import PostViewSet
from .views.posts_batch import PostBatchView
from .views.img import img_view


app_name = 'api'

router = routers.DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'blogs', BlogViewSet)
router.register(r'posts', PostViewSet)


urlpatterns = [
	url(r'^$', RootView.as_view(), name='root'),
	url(r'^session/', SessionView.as_view(), name='session'),
	url(r'^posts/batch', PostBatchView.as_view(), name='posts-batch'),
	url(r'^', include(router.urls)),
	# session
	# users
	# blogs/<pk>/tags	GET
	# tags				GET
	# posts/<slug>/comments
	# comments
	url(r'^img/', img_view),
	# url(r'^', include('rest_framework.urls')),
]