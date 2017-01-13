from django.conf.urls import url, include
from rest_framework import routers
from .views.posts import PostViewSet
from .views.comments import CommentViewSet
from .views.img import img_view


app_name = 'api'

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
# router.register(r'comments', CommentViewSet)


_ = '''
parameter: filter_by, order_by, search, page
parameter: all_blog, blog_id, blog_domain

GET:	posts/			?tags, 
POST:	posts/			?content, title, tags
GET:	posts/<p>
PUT:	posts/<p>
DELETE:	posts/<p>

DELETE: posts/	{delete_slugs: ['', '', ...]}

GET:	comments/		?post_slug, 
POST:	comments/		?post_slug, 

GET:	posts/<p>/tags/
POST:	posts/<p>/tags/

GET:	posts/<p>/comments/
POST:	posts/<p>/comments/

POST:	img/
'''
urlpatterns = [
	url(r'^', include(router.urls)),
	url(r'^img/', img_view),
	# url(r'^', include('rest_framework.urls')),
]