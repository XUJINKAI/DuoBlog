import Vue from 'vue'

export {BUS, API};

var BUS = new Vue({
	template: '<div></div>',
	data: function(){
		return {
			blogs_list: []
		}
	}
});
Vue.use(function(Vue){
	Vue.prototype.BUS = BUS;
	Vue.mixin({
		created: function(){
			this.$data.$BUS = BUS;
		}
	})
});


var API_URL = function(key){
	var maps = {
		blog_list: '/api/blogs/',
		post_list: '/api/posts/',
	}
	return maps[key];
}

var API = {
	blog_list: function(callback) {
		get_data(API_URL('blog_list'), {}, function(data) {
			if(callback) callback(data);
		});
	},
	post_parameter: function(post){
		return _.omitBy({
			slug: post.slug,
			title: post.title,
			content: post.content,
			content_type: post.content_type,
			rendered_html: post.rendered_html,
			status: post.status,
			tags: JSON.stringify(post.tags),
			comments: post.comments,
			sticky: post.sticky,
		}, _.isNil)
	},
	post_list: function(filter, callback) {
		get_data(API_URL('post_list'), filter, function(data){
			if(callback) callback(data);
		})
	},
	post_detail: function(post, callback) {
		if(post.api_url) {
			get_data(post.api_url, {}, function(data){
				if(callback) callback(data);
			})
		} else {
			callback();
		}
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
};


		API.blog_list(function(data){
			log(data);
		})