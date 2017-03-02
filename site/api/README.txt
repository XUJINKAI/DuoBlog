API Design:

ROOT:
/blogs/
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