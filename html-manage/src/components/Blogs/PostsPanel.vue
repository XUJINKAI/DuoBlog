<template>
	<div class="wrapper">
		<div class="left stretch full-height">
			<div class="status">
				<span style="font-weight: bolder;">Status:</span>
				<br>
				<input type="radio" value="" id="all" v-model='filter_status'>
				<label for="all">All ({{posts_all_count}})</label>
				<br>
				<input type="radio" value="s" id="sticky" v-model='filter_status'>
				<label for="sticky">Sticky ({{posts_sticky_count}})</label>
				<br>
				<input type="radio" value="p" id="public" v-model='filter_status'>
				<label for="public">Public ({{posts_public_count}})</label>
				<br>
				<input type="radio" value="h" id="hidden" v-model='filter_status'>
				<label for="hidden">Hidden ({{posts_hidden_count}})</label>
				<br>
				<input type="radio" value="x" id="private" v-model='filter_status'>
				<label for="private">Private ({{posts_private_count}})</label>
			</div>
			<br>
			<div class="tags">
				<span style="font-weight: bolder;">Tags: </span>
				<span @click='' class='clear_tags'>Clear</span>
				<p v-for='tag in tags'>
					<input type="checkbox" :id="tag.name" :value='tag' v-model='selected_tags'>
					<span :for='tag.name' @click='select_tag(tag);'>{{ tag.name }} {{ tag.count }}</span>
				</p>
			</div>
		</div>
		<div class="right stretch box-col">
			<div class="new-post box">
				<button class="stretch" @click='new_markdown'>Markdown</button>
				<button class="stretch" @click='new_html'>HTML</button>
			</div>
			<div class="posts-div box-col">
				<div class="posts-order">
					<input class="select-all" type="checkbox" @click='select_all' v-model='is_select_all'>
					<span class="posts-order-btn" :class='{bolder: order_by=="title"}' @click='change_order("title")'>
						Title <span v-if='order_by=="title"'>{{ order_asc?'↑':'↓'}}</span>
					</span>
					<span class="posts-order-btn" :class='{bolder: order_by=="create"}' @click='change_order("create")'>
						Create <span v-if='order_by=="create"'>{{ order_asc?'↑':'↓'}}</span>
					</span>
					<span class="posts-order-btn" :class='{bolder: order_by=="modify"}' @click='change_order("modify")'>
						Modify <span v-if='order_by=="modify"'>{{ order_asc?'↑':'↓'}}</span>
					</span>
				</div>
				<div class="posts-list">
					<p
						v-for='post in posts_show_list'
						:id='post.pk'
						class="post-item"
						:class="{selected: is_post_selected(post)}"
						@click="click_post_item($event, post)"
					>
						<span v-if='post.title' class="post-title">{{ post.title }}</span>
						<span class="post-abstract">{{ post.abstract }}</span>
						<span class="post-info">
							<span class="post-time">
								<span v-if='order_by=="modify"'>{{ post.last_modified_time | fromNow }}</span>
								<span v-else>{{ post.create_time | fromNow }}</span>
							</span>
							<span class="post-comment">
								<span v-if='post.comments'><i class="fa fa-comment-o" aria-hidden="true"></i></span>
							</span>
							<span class="post-status">
								<span v-if='post.status=="s"'><i class="fa fa-thumb-tack" aria-hidden="true"></i></span>
								<span v-if='post.status=="x"'><i class="fa fa-lock" aria-hidden="true"></i></span>
								<span v-if='post.status=="h"'><i class="fa fa-eye-slash" aria-hidden="true"></i></i></span>
							</span>
						</span>
					</p>
				</div>
			</div>
		</div>
		<div class="posts-detail stretch">
			<router-view v-if='is_select_one_post' @save='post_saved'></router-view>
			<MultiEditor
				v-else-if='is_select_multi_post'
				:posts='selected_posts'
				@delete_all='selected_delete'
				>
			</MultiEditor>
			<p v-else>no selected</p>
		</div>
	</div>
</template>

<script>
import MultiEditor from './PostsPanel/PostsMultiEditor'

export default {
	components: {
		MultiEditor,
	},
	data: function(){
		return {
			all_posts: [],

			filter_status: '',
			selected_tags: [],
			selected_posts: [],

			order_by: 'create',
			order_asc: false,
		};
	},
	computed: {
		blog_pk: function() {
			return this.$route.params.blog;
		},

		posts_all_count: function(){
			return this.all_posts.length;
		},
		posts_sticky_count: function(){
			return _.filter(this.all_posts, {status: 's'}).length;
		},
		posts_public_count: function(){
			return _.filter(this.all_posts, {status: 'p'}).length;
		},
		posts_hidden_count: function(){
			return _.filter(this.all_posts, {status: 'h'}).length;
		},
		posts_private_count: function(){
			return _.filter(this.all_posts, {status: 'x'}).length;
		},

		tags: function(){
			var tags_list = [];
			_.forEach(this.all_posts, function(post){
				tags_list = _.concat(tags_list, post.tags)
			});
			var tags_count = _.countBy(tags_list);
			var tags_coll = [];
			_.forEach(tags_count, function(value, key){
				tags_coll.push({
					name: key,
					count: value,
				})
			})
			return _.orderBy(tags_coll, ['count', 'name'], ['desc', 'asc'])
		},

		posts_show_list: function(){
			var tmp = [];

			if(this.filter_status !== '') {
				tmp = _.filter(this.all_posts, {status: this.filter_status});
			} else {
				tmp = this.all_posts;
			}

			var order_by = this.order_by;
			var order;
			if(this.order_asc) {
				order = 'asc';
			} else {
				order = 'desc';
			}
			if(order_by=='create') order_by = 'create_time';
			if(order_by=='modify') order_by == 'last_modified_time';
			if(order_by=='title') {
				tmp = _.orderBy(tmp, ['title', 'abstract'], [order, order]);
			} else {
				tmp = _.orderBy(tmp, [order_by], [order]);
			}
			
			return tmp;
			// if(this.selected_tags.length==0) {
			// 	return this.all_posts;
			// } else {
			// 	var self = this;
			// 	return _.filter(self.all_posts, function(post){
			// 		var flag = true;
			// 		_.forEach(self.selected_tags, function(t){
			// 			if(!_.includes(post.tags, t.name)) {
			// 				flag = false;
			// 			}
			// 		});
			// 		return flag;
			// 	});
			// }
		},
		is_select_one_post: function(){
			return this.selected_posts.length == 1;
		},
		is_select_multi_post: function(){
			return this.selected_posts.length > 1;;
		},
		is_select_all: function(){
			var l = this.selected_posts.length;
			if (l <= 1) {
				return false;
			}
			return this.selected_posts.length == this.posts_show_list.length;
		},
	},
	watch: {
		'$route.params.blog': function(){
			if(this.$route.name.startsWith('post')) {
				this.reload_all_posts();
			}
		},
		'$route': function(){
			if(this.$route.name=='post-detail') {
				this.on_router_changed();
			}
		},
	},
	methods: {
		reload_all_posts: function(callback){
			var self = this;
			this.BUS.load_post_list({
				blog: self.blog_pk,
				deleted: false
			}, function(data){
				self.all_posts = data;
				if(callback) callback();
			})
		},
		on_selected_posts_changed: function(){
			if(this.is_select_one_post) {
				this.$router.push({ name: 'post-detail', params: {blog: this.blog_pk, post: this.selected_posts[0].pk }})
			} else {
				this.$router.push({ name: 'post-list', params: {blog: this.blog_pk }})
			}
		},
		on_router_changed: function(){
			if(this.$route.name=='post-detail') {
				var pk = parseInt(this.$route.params.post);
				if(_.filter(this.selected_posts, {pk: pk}).length==0) {
					this.filter_status = '';
				}
				this.selected_posts = _.filter(this.all_posts, {pk: pk});
			}
		},

		change_order: function(value) {
			if(value==this.order_by) {
				this.order_asc = !this.order_asc;
			} else {
				this.order_by = value;
				if(value=='title') {
					this.order_asc = true;
				} else {
					this.order_asc = false;
				}
			}
		},

		clear_tags: function(){
			this.selected_tags = [];
		},
		select_tag: function(tag){
			this.clear_tags();
			this.selected_tags = [tag];
		},

		new_markdown: function(){
			this.create_new_post('m');
		},
		new_html: function(){
			this.create_new_post('h');
		},
		create_new_post: function(type) {
			var self = this;
			self.BUS.suppress_router(function(release_suppress){
				self.BUS.create_new_post(type, self.blog_pk, function(data){
					self.all_posts.unshift(data);
					self.on_router_changed();
				});
				release_suppress();
			})
		},
		// posts-list
		is_post_selected: function(post){
			return this.selected_posts.includes(post);
		},
		click_post_item: function(event, post){
			if(event.ctrlKey) {
				if(this.is_post_selected(post)) {
					this.selected_posts.remove(post);
				} else {
					this.selected_posts.push(post);
				}
			} else {
				if(this.selected_posts.length==1 && this.selected_posts[0]==post) {
					this.selected_posts = [];
				} else {
					this.selected_posts = [post];
				}
			}
			this.on_selected_posts_changed();
		},

		selected_change: function(data){
			this.selected_posts = data;
		},
		select_all: function() {
			if(this.is_select_all) {
				this.selected_posts = [];
			} else {
				this.selected_posts = [];
				var self = this;
				this.all_posts.forEach(function(post){
					self.selected_posts.push(post);
				});
			}
		},
		// batch
		selected_delete: function(){
			var self = this;
			var delete_pks = [];
			self.selected_posts.forEach(function(post){
				delete_pks.push(post.pk);
			})
			self.BUS.delete_posts_batch(delete_pks, function(){
				self.reload_all_posts();
				self.BUS.reload_blog_list();
				self.selected_posts = [];
				self.on_selected_posts_changed();
			});
		},

		post_saved: function(post){
			var p = _.filter(this.all_posts, {pk: post.pk})
			if(p.length==1) {
				p = p[0];
				_.forEach(post, function(value, key){
					p[key] = value;
				})
			}
		},
	},
	filters: {
		fromNow: function(time) {
			return moment(time).fromNow();
		}
	},
	created: function(){
		var self = this;
		self.BUS.$on('post_list_changed', function(){
			self.reload_all_posts();
			self.selected_posts = [];
		});
	},
	mounted: function(){
		var self = this;
		self.BUS.run_after(function(){
			self.reload_all_posts(function(){
				self.on_router_changed();
			})
		},'login');
	}
}
</script>

<style scoped>
.wrapper {
	padding-left: 5px;
	flex: 1;
	display: flex;
	height: calc(100% - 5px);
}
.left {
	height: 100%;
	flex: 0 0 150px;
}
.right {
	height: 100%;
	flex: 0 0 200px;
}
.new-post {
	flex: 0 0 34px;
}
.new-post button {
	flex: 1;
	margin-bottom: 10px;
}
.posts-detail {
	height: 100%;
	width: 100%;
	padding: 0 0 0 20px;
	flex: 1;
}


.posts-order {
	/*justify-content: space-between;*/
	flex: 0 0 1.9em;
	display: flex;
}
.select-all {
	flex: 0 0 15px;
}
.posts-order-btn {
	flex: 1 0 30%;
	cursor: pointer;
}

.posts-list {
	height: 100%;
	list-style: none;
	margin: 0;
	padding: 0;
	flex: 1;
	overflow-y: scroll;
}
.posts-list p.post-item {
	height: 100px;
	border: solid 1px rgba(77, 79, 77, 0.27);
	margin-top: 0;
	margin-bottom: 2px;
	display: flex;
	flex-direction: column;
	cursor: default;
	padding: 4px;
}
.post-item .post-title {
	flex: 0 0 18px;
	font-weight: bold;
	word-break: break-all;
	overflow-y: hidden;
}
.post-item .post-abstract {
	flex: 1;
	word-break: break-all;
	overflow-y: hidden;
	background: -webkit-linear-gradient(black, gray);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
}
.post-item .post-time {
	font-size: 12px;
}
.post-item .post-info {
	flex: 0 0 13px;
	font-size: 12px;
	display: flex;
	justify-content: space-between;
}
.post-info .post-time {
	flex: 1;
	font-style: italic;
}
.post-info .post-comment {
	flex: 0 0 26px;
	color: rgba(0, 0, 0, .35);
}
.post-info .post-status {
	flex: 0 0 18px;
}
.post-item .post-status .fa-thumb-tack{
	color: red;
}
.posts-list p input {
	display: none;
}
.selected {
	background-color: #d9d9d9;
}
</style>
