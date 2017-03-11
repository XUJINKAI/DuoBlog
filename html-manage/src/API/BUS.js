import Vue from 'vue'

export default BUS;

var BUS = new Vue({
	data: {
		_blog_list: [],
		_blog__pk: -1,
		_blog__btn: 'posts',

		_post_list: [],
		_post__slug: '',

		_post_detail: null,
		_post_changed: false,
	},
	computed: {
		time_format: function(){
			return 'YYYY-MM-DD HH:mm:ss';
		},

		blog_list: function(){
			return this.$data._blog_list;
		},
		current_blog: function(){
			var f = _(this.blog_list).find(['pk', this.$data._blog__pk]);
			if( ! f) {
				f = this.blog_list[0];
				this.$data._blog__pk = f.pk;
				this.reload_post_list();
			}
			return f;
		},
		current_blog_btn: function(){
			return this.$data._blog__btn;
		},
		current_blog_btn_status: function(){
			var l = {
				posts: 'p',
				draft: 'd',
				trash: 't',
			}
			return l[this.current_blog_btn];
		},

		post_list: function(){
			return this.$data._post_list;
		},
		current_post: function(){
			var f = _(this.post_list).find(['slug', this.$data._post__slug]);
			if ( ! f) {
				return {};
			}
			return f;
		},

		post_detail: function(){
			return this.$data._post_detail;
		},

		post_changed: function(){
			return this.$data._post_changed && this.post_detail;
		},
		ask_quit: function(){
			return this.post_changed;
		},
	},
	watch: {
		post_detail: {
			deep: true,
			handler: function(val, oldVal){
				this.$data._post_changed = true;
			},
		},
		post_changed: function(){
			log('BUS.post_changed = '+this.$data._post_changed);
		},
	},
	methods: {
		reload_blog_list: function(){
			var self = this;
			API.blog_list(function(data){
				self.$data._blog_list = data;
			})
		},
		select_blog_function: function(blog, btn){
			this.$data._blog__pk = blog.pk;
			this.$data._blog__btn = btn;
			this.reload_post_list();
			this.$data._post_detail = null;
		},
		create_new_blog: function(){
			log('//TODO')
		},

		reload_post_list: function(){
			var self = this;
			API.post_list({
				pk: self.current_blog.pk,
				status: self.current_blog_btn_status,
			}, function(data){
				self.$data._post_list = data;
			})
		},
		select_post: function(post){
			this.$data._post__slug = post.slug;
			this.reload_post_detail();
		},
		create_new_post: function(type){
			var self = this;
			API.post_new({
				status: 'p',
				content: 'your new post',
				rendered_html: 'your new html post',
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

		reload_post_detail: function(){
			var self = this;
			var handler = function(){
				API.post_detail(self.current_post, function(data){
					self.$data._post_detail = data;
					setTimeout(function(){
						self.$data._post_changed = false;
					}, 0);
				})
			}
			if(self.post_changed) {
				self.save_post_detail(false, function(){
					handler();
				})
			} else {
				handler();
			}
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
	}
});
Vue.use(function(Vue){
	Vue.prototype.BUS = BUS;
	Vue.mixin({
		created: function(){
			this.BUS = BUS;
			this.$data.$BUS = BUS.$data;
		}
	})
});
