import Vue from 'vue'

export default BUS;

var BUS = new Vue({
	data: {
		_session: null,
		_blog_list: [],

		_ori_content: null,
		_content: null,
		_save_handler: null,

		modal_login: null,
		modal_save_no_cancel: null,
		modal_blog_delete: null,
	},
	computed: {
		time_format: function(){
			return 'YYYY-MM-DD HH:mm:ss';
		},
		username: function(){
			if(this.is_login){
				return this.$data._session.username;
			} else {
				return 'Not_Login';
			}
		},
		is_login: function(){
			if( ! this.$data._session) {
				return false;
			} else {
				return true;
			}
		},
		blog_list: function(){
			return this.$data._blog_list;
		},
		content_changed: function(){
			return JSON.stringify(this.$data._ori_content) !== JSON.stringify(this.$data._content)
		},
		ask_quit: function(){
			return this.content_changed;
		},
	},
	watch: {
		content_changed: function(){
			if(window.DEBUG) {
				log('BUS.content_changed = '+this.content_changed);
			}
		},
	},
	methods: {
		on_router_change: function(to, from, next){
			this.check_content_saved(function(clear){
				if(clear) {
					next();
				} else {
					next(false);
				}
			})
		},

		login: function(username, password){
			var self = this;
			API.login(username, password, function(session){
				self.$data._session = session;
			})
		},
		check_login: function(callback){
			if(this.is_login){
				callback();
			}
		},

		set_content: function(obj, save_handler){
			if( ! save_handler) {
				alert('网页出错：BUS.set_content must have a save_handler')
			}
			this.$data._ori_content = JSON.parse(JSON.stringify(obj));
			this.$data._content = obj;
			this.$data._save_handler = save_handler;
		},
		clear_content: function(){
			this.$data._ori_content = null;
			this.$data._content = null;
		},
		check_content_saved: function(cb_clear){
			var self = this;
			if(this.content_changed) {
				self.modal_save_no_cancel(function(result){
					if(result=='save') {
						self.$data._save_handler()
						cb_clear(true);
					} else if (result=='no') {
						self.clear_content();
						cb_clear(true);
					} else {
						cb_clear(false);
					}
				})
			} else {
				cb_clear(true);
			}
		},

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
		_delete_blog: function(blog){
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
		delete_blog: function(blog){
			var self = this;
			self.modal_blog_delete(function(result){
				if(result=='delete') {
					self._delete_blog(blog);
				}
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
		self.check_login(function(){
			self.reload_blog_list();
		})
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
