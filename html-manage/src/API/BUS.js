import Vue from 'vue'

export default BUS;

var BUS = new Vue({
	data: {
		_blog_list: [],
		content_changed: false,
	},
	computed: {
		time_format: function(){
			return 'YYYY-MM-DD HH:mm:ss';
		},
		blog_list: function(){
			return this.$data._blog_list;
		},
		ask_quit: function(){
			return this.content_changed;
		},
	},
	watch: {
		content_changed: function(){
			log('BUS.content_changed = '+this.content_changed);
		},
	},
	methods: {
		reload_blog_list: function(callback, emit=true){
			var self = this;
			API.blog_list(function(data){
				self.$data._blog_list = data;
				if(emit) self.$emit('blog_changed');
				if(callback) callback(data);
			})
		},
		create_new_blog: function(){
			var self = this;
			API.blog_new(function(data){
				self.reload_blog_list(function(){
					self.$emit('blog_changed', data.pk);
				}, false);
			})
		},
		delete_blog: function(blog){
			var self = this;
			var f = _.find(this.blog_list, {'pk': blog.pk})
			var idx = this.blog_list.indexOf(f);
			API.blog_delete(blog.pk, function(data){
				self.reload_blog_list(function(blog_list){
					var len = blog_list.length;
					if(idx >= len) {
						idx = len - 1;
					}
					var pk = blog_list[idx].pk;
					self.$emit('blog_changed', pk);
				}, false);
			})
		},
		save_blog: function(blog, callback){
			var self = this;
			API.blog_update(blog, function(data){
				self.reload_blog_list();
				if(callback) callback(data);
			})
		},

		create_new_post: function(type){
			var self = this;
			API.post_new({
				status: 'd',
				content: '',
				rendered_html: '<p/>',
				content_type: type,
				tags: [],
			}, function(data){
				self.reload_blog_list();
				self.reload_post_list();
				self.$data._post__slug = data.slug;
				self.$data.current_post = data;
				self.reload_post_detail();
			})
		},

		save_post_detail: function(type, callback){
			var self = this;
			if(type) {
				self.post_detail.status = type;
			}
			API.post_update(self.post_detail, function(){
				self.$data._post_changed = false;
				self.reload_blog_list();
				self.reload_post_list();
				if(callback) callback();
			})
		},
		save_post_detail_public: function(){
			this.save_post_detail('p');
		},
		save_post_detail_draft: function(){
			this.save_post_detail('d');
		},
		delete_post_detail: function(){
			var self = this;
			API.post_delete(this.post_detail, function(){
				self.reload_blog_list();
				self.reload_post_list();
				self.$data._post__slug = -1;
				self.$data._post_detail = null
			});
		},
	},
	created: function(){
		var self = this;
		window.onbeforeunload = function(event) {
			if(self.ask_quit) {
				return "确定退出吗";
			}
		}
		this.reload_blog_list();
	},
});
Vue.use(function(Vue){
	Object.defineProperty(Vue.prototype, '$BUS', {
		get () { return BUS.$data }
	})

	Object.defineProperty(Vue.prototype, 'BUS', {
		get () { return BUS }
	})
});
