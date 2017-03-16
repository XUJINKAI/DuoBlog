import Vue from 'vue'
import {API} from './API'

export default BUS;

var BUS = new Vue({
	data: {
		_session: {login: true, username: 'Not_Login'},
		_blog_list: [],

		_ori_content: null,
		_content: null,
		_auto_save: false,
		_save_handler: null,

		_bln_suppress_router: false,

		modal_login: null,
		modal_save_no_cancel: null,
		modal_blog_delete: null,
	},
	computed: {
		time_format: function(){
			return 'YYYY-MM-DD HH:mm:ss';
		},
		bln_suppress_router: function(){
			return this.$data._bln_suppress_router;
		},
		is_login: function(){
			if( ! this.$data._session) {
				return false;
			} else {
				return this.$data._session.login;
			}
		},
		username: function(){
			if(this.is_login){
				return this.$data._session.username;
			} else {
				return 'Not_Login';
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
				// log(JSON.stringify(this.$data._ori_content));
				// log(JSON.stringify(this.$data._content));
			}
		},
	},
	methods: {
		/*
		suppress_router(function(release_suppress){
			// Do something
			release_suppress(<after_suppress>);
		})
		*/
		suppress_router: function(in_suppress){
			if( ! in_suppress) {
				alert('Error: BUS.suppress_router must has callback in_suppress');
				return;
			}
			var self = this;
			self.$data._bln_suppress_router = true;
			in_suppress(function(after_suppress){
				self.$data._bln_suppress_router = false;
				if(after_suppress) after_suppress();
			})
		},
		// hook to router.beforeEach in main.js
		on_router_change: function(to, from, next){
			var self = this;
			self.check_content_saved(function(clear){
				if(clear) {
					var suppress = self.$data._bln_suppress_router;
					next( ! suppress);
				} else {
					next(false);
				}
			})
		},
		// session
		reload_session(){
			var self = this;
			API.login_status(function(data){
				self.$data._session = data;
				if(self.is_login) {
					API.SET_MODE(data.role);
					self.reload_blog_list();
				}
			})
		},
		login: function(username, password){
			var self = this;
			if(username=='' || password=='') {
				self.$message({
					message: '请输入信息',
					type: 'warning'
				});
				return;
			}
			API.login(username, password, function(data){
				self.$data._session = data;
				if(self.is_login) {
					self.reload_blog_list();
					self.$message({
						message: '登录成功',
						type: 'success'
					});
				} else {
					self.$message.error('登录失败');
				}
			})
		},
		logout: function(){
			var self = this;
			API.logout(function(data){
				self.$data._session = data;
			});
		},
		// global content change modal
		set_content: function(obj, save_handler, auto_save=false){
			if( ! save_handler) {
				alert('网页出错：BUS.set_content must have a save_handler')
			}
			log('BUS.set_content')
			this.$data._ori_content = JSON.parse(JSON.stringify(obj));
			this.$data._content = obj;
			this.$data._save_handler = save_handler;
			this.$data._auto_save = auto_save;
		},
		clear_content: function(){
			log('BUS.clear_content')
			this.$data._ori_content = null;
			this.$data._content = null;
		},
		check_content_saved: function(cb_clear){
			var self = this;
			if(self.content_changed) {
				if(self.$data._auto_save) {
					self.$data._save_handler();
					cb_clear(true);
				} else {
					self.modal_save_no_cancel(function(result){
						if(result=='save') {
							self.$data._save_handler();
							cb_clear(true);
						} else if (result=='no') {
							self.clear_content();
							cb_clear(true);
						} else {
							cb_clear(false);
						}
					})
				}
			} else {
				cb_clear(true);
			}
		},
		// blog
		reload_blog_list: function(callback, emit=true){
			var self = this;
			API.blog_list(function(data){
				self.$data._blog_list = data;
				if(emit) self.$emit('blog_changed');
				if(callback) callback(data);
			})
		},
		load_blog: function(pk, callback){
			API.blog_detail(pk, callback);
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
				self.$emit('blog_saved', data);
				if(callback) callback(data);
			})
		},
		// post
		router_open_post: function(post){
			this.$emit('router_open_post', 'post', post.pk, post.blog);
		},
		load_post: function(pk, callback){
			API.post_detail(pk, function(data){
				if(callback) callback(data);
			})
		},
		load_post_list: function(callback, parameter){
			API.post_list(parameter, callback);
		},
		create_new_post: function(type, blog_pk, callback){
			var self = this;
			API.post_new({
				blog: blog_pk,
				content: '',
				content_type: type,
				rendered_html: '<p/>',
				tags: [],
			}, function(data){
				self.reload_blog_list();
				self.router_open_post(data);
				if(callback) callback(data);
			})
		},
		save_post: function(post, callback){
			var self = this;
			API.post_update(post, function(data){
				// ! 顺序很重要，callback会先设置set_content，
				// 这样后续的操作才不会提醒未保存，
				// 最先callback，最后$emit
				if(callback) callback(data);
				self.reload_blog_list();
				self.router_open_post(data);
				self.$emit('post_saved');
			})
		},
		delete_post: function(post, callback){
			var self = this;
			API.post_delete(post, function(){
				self.reload_blog_list();
				self.$emit('post_list_changed');
				self.$emit('post_deleted')
				if(callback) callback();
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
		this.reload_session();
	},
});
Vue.use(function(Vue){
	Object.defineProperty(Vue.prototype, '$BUS', {
		get () { return BUS.$data }
	})

	Object.defineProperty(Vue.prototype, 'BUS', {
		get () { return BUS }
	})

	Vue.mixin({
		created: function(){
			this.$data.$BUS = BUS.$data;
		}
	})
});
