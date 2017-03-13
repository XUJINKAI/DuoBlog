var API_URL = function(key){
	var maps = {
		session: '/api/session/',
		blog_list: '/api/blogs/',
		post_list: '/api/posts/',
	}
	return maps[key];
}

var API = {
	login_status: function(callback) {
		get_data(API_URL('session'), {}, function(data){
			if(callback) callback(data);
		})
	},
	login: function(username, password, callback){
		post_data(API_URL('session'), {
			username: username,
			password: password,
		}, function(data){
			if(callback) callback(data);
		})
	},
	logout: function(callback) {
		delete_data(API_URL('session'), {}, function(data){
			if(callback) callback(data);
		})
	},

	blog_parameter: function(blog){
		return _.omitBy({
			name: blog.name,
			url: blog.url,
			desc: blog.desc,
			navs: blog.navs,
			theme: blog.theme,
			rss: blog.rss,
			sitemap: blog.sitemap,
			comments: blog.comments,
			custom_comment_html: blog.custom_comment_html,
			head_html: blog.head_html,
			body_html: blog.body_html,
		}, _.isNil)
	},
	blog_list: function(callback) {
		get_data(API_URL('blog_list'), {}, function(data) {
			if(callback) callback(data);
		});
	},
	blog_new: function(callback) {
		post_data(API_URL('blog_list'), {
			name: 'NewBlog',
			url: Math.random().toString(36).substring(8),
		}, function(data){
			if(callback) callback(data);
		});
	},
	blog_detail: function(pk, callback) {
		get_data(API_URL('blog_list') + pk, {}, function(data){
			if(callback) callback(data);
		})
	},
	blog_delete: function(pk, callback) {
		delete_data(API_URL('blog_list') + pk, {}, function(data){
			if(callback) callback(data);
		})
	},
	blog_update: function(blog, callback) {
		put_data(API_URL('blog_list') + blog.pk + '/', API.blog_parameter(blog), function(data){
			if(callback) callback(data);
		})
	},

	post_parameter: function(post){
		return _.omitBy({
			blog: post.blog,
			slug: post.slug,
			title: post.title,
			content: post.content,
			content_type: post.content_type,
			rendered_html: post.rendered_html,
			status: post.status,
			sticky: post.sticky,
			comments: post.comments,
			tags: JSON.stringify(post.tags),
		}, _.isNil)
	},
	post_list: function(filter, callback) {
		get_data(API_URL('post_list'), filter, function(data){
			if(callback) callback(data);
		})
	},
	post_detail: function(pk, callback) {
		get_data(API_URL('post_list') + pk, {}, function(data){
			if(callback) callback(data);
		})
	},
	post_new: function(post, callback){
		post_data(API_URL('post_list'), API.post_parameter(post), function(data){
			if(callback) callback(data);
		})
	},
	post_update: function(post, callback) {
		put_data(post.api_url, API.post_parameter(post), function(data){
			if(callback) callback(data);
		})
	},
	post_delete: function(post, callback) {
		delete_data(post.api_url, {}, function(data){
			if(callback) callback(data);
		})
	},
	EDIT_HTML: function(id, change) {
		log('EDIT_HTML: init html editor')
		var editor = new wangEditor(id);
		editor.config.jsFilter = false;
		editor.config.uploadImgUrl = '/api/img/';
		editor.config.uploadHeaders = {
		'X-CSRFToken': getCookie('csrftoken'),
		};
		editor.config.uploadImgFileName = 'file'
		editor.onchange = function(){
		change(editor);
		}
		editor.create();
		return editor;
	}
};