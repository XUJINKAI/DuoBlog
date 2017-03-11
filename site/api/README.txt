API Design:
要点：
登录与否，应该只影响权限，尽量与展示的项目无关，避免登录以后就能看到更多项目这种事发生，要看到更多内容应该访问不同的地址。


URL, GROUP, METHOD, PERMISSION
/posts/, GUEST, GET, True
/posts/, GUEST, POST, False

ROOT:

Admin
/blogs/			GET
				POST
/blogs/<pk>		GET, PUT, DEL


Admin
/posts/



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