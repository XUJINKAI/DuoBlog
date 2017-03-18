export var API_URL = function(key){
	var maps = {
		session: '/api/session/',
		blog_list: '/api/blogs/',
		post_list: '/api/posts/',
		posts_batch: '/api/posts/batch',
	}
	return maps[key];
}
var blog_parameter = function(blog){
	return _.omitBy({
		name: blog.name,
		domain: blog.domain,
		absolute_url: blog.absolute_url,
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
}
var post_parameter = function(post){
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
}

export var API = {
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
	// blog
	blog_list: function(callback) {
		get_data(API_URL('blog_list'), {}, function(data) {
			if(callback) callback(data);
		});
	},
	blog_new: function(callback) {
		post_data(API_URL('blog_list'), {
			name: 'NewBlog',
			domain: Math.random().toString(36).substring(2),
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
		put_data(API_URL('blog_list') + blog.pk + '/', blog_parameter(blog), function(data){
			if(callback) callback(data);
		})
	},
	// post
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
		post_data(API_URL('post_list'), post_parameter(post), function(data){
			if(callback) callback(data);
		})
	},
	post_update: function(post, callback) {
		put_data(post.api_url, post_parameter(post), function(data){
			if(callback) callback(data);
		})
	},
	post_delete: function(post, callback) {
		delete_data(post.api_url, {}, function(data){
			if(callback) callback(data);
		})
	},
};
//ajax
function ajax_data(method, url, data, success, error, complete) {
	if(!method || !url) throw 'Bad request: No method or url';
	url = TrimUrl(url);
	return $.ajax({
		url: url,
		method: method,
		headers: {
			'X-CSRFToken': getCookie('csrftoken'),
		},
		dataType: 'json',
		data: data,
		success: function(result) {
			log('%c' + method + ': ' + url, 'color: red; background-color: rgba(206, 206, 206, 0.45);');
			log(data);
			log(result);
			if(success) { success(result); }
		},
		error: function(result) {
			log(result.responseText);
			if(window._AJAX_ERROR) {window._AJAX_ERROR(result)}
			if(error) { error(result); }
		},
		complete: function(result) {
			if(complete) { complete(result); }
		},
	})
}

function get_data(url, data, success, error, complete) {
	return ajax_data('GET', url, data, success, error, complete)
}
function post_data(url, data, success, error, complete) {
	return ajax_data('POST', url, data, success, error, complete);
}
function put_data(url, data, success, error, complete) {
	return ajax_data('PUT', url, data, success, error, complete);
}
function patch_data(url, data, success, error, complete) {
	return ajax_data('PATCH', url, data, success, error, complete);
}
function delete_data(url, data, success, error, complete) {
	return ajax_data('DELETE', url, data, success, error, complete);
}
export var ajax = {
	get: get_data,
	post: post_data,
	put: put_data,
	patch: patch_data,
	delete: delete_data,
}

function TrimUrl(url) {
	return url.replace(/https?:\/\/[^\/]+/i, "");
}
export function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

window.log = function(){
	if(typeof(DEBUG)=='boolean'&&DEBUG){
		console.log.apply(this, arguments);
	}
}
// Array
Array.prototype.remove = function() {
	var what, a = arguments, L = a.length, ax;
	while (L && this.length) {
		what = a[--L];
		while ((ax = this.indexOf(what)) !== -1) {
			this.splice(ax, 1);
		}
	}
	return this;
};
Array.prototype.move = function (old_index, new_index) {
	if(old_index<0 || old_index>=this.length 
		|| new_index<0 || new_index>=this.length){
		return this;
	}
	if (new_index >= this.length) {
		var k = new_index - this.length;
		while ((k--) + 1) {
			this.push(undefined);
		}
	}
	this.splice(new_index, 0, this.splice(old_index, 1)[0]);
	return this; // for testing purposes
};