<template>
	<div class="wrapper box stretch full-height">
		<div class="left stretch full-height">
			<span style="font-weight: bolder;">Status:</span>
			<ul>
				<li @click=''>
					<input type="radio" name="">
					<span>All</span>
				</li>
				<li>sticky</li>
				<li>public</li>
				<li>hidden</li>
				<li>private</li>
			</ul>
			<div>
				<span style="font-weight: bolder;">Tags: </span>
				<span @click='' class='clear_tags'>Clear</span>
				<ul>
					<li v-for='tag in tags'>
						<input type="checkbox" :id="tag.name" :value='tag' v-model='selected_tags'>
						<span :for='tag.name' @click='select_tag(tag);'>{{ tag.name }} {{ tag.count }}</span>
					</li>
				</ul>
			</div>
		</div>
		<div class="right stretch box-col">
			<div class="new-post box">
				<button class="stretch" @click='new_markdown'>Markdown</button>
				<button class="stretch" @click='new_html'>HTML</button>
			</div>
			<div class="posts-div box-col">
				<div class="posts-order box">
					<input type="checkbox" @click='select_all' :bind='is_select_all'>
					<span :class='{bolder: order_by=="title"}'>Title <span v-if='order_by=="title"'>{{ order_asc?'↑':'↓'}}</span></span>
					<span :class='{bolder: order_by=="create"}'>Create <span v-if='order_by=="create"'>{{ order_asc?'↑':'↓'}}</span></span>
					<span :class='{bolder: order_by=="modify"}'>Modify <span v-if='order_by=="modify"'>{{ order_asc?'↑':'↓'}}</span></span>
				</div>
				<ul class="posts-ul">
					<li
						v-for='post in posts_show' :key='post.pk'
						class="post-item"
						:class="{selected: is_selected(post)}"
						@click='select_post($event, post)'
						>
						<input type="checkbox" value='post' v-model='selected_posts'>
						<p>{{ post.abstract }}</p>
						<!-- <span>{{ post.last_modified_time }}</span> -->
					</li>
				</ul>
			</div>
		</div>
		<div class="posts-detail stretch">
			<router-view v-if='is_select_one_post'></router-view>
			<p v-else-if='is_select_multi_post'>multi selected</p>
			<p v-else>no selected</p>
		</div>
	</div>
</template>

<script>
export default {
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
		is_select_all: function(){
			return this.posts_show.every(this.is_selected);
		},
		posts_show: function(){
			if(this.selected_tags.length==0) {
				return this.all_posts;
			} else {
				var self = this;
				return _.filter(self.all_posts, function(post){
					var flag = true;
					_.forEach(self.selected_tags, function(t){
						if(!_.includes(post.tags, t.name)) {
							flag = false;
						}
					});
					return flag;
				});
			}
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
		is_select_one_post: function(){
			return this.selected_posts.length == 1;
		},
		is_select_multi_post: function(){
			return this.selected_posts.length > 1;;
		},
	},
	watch: {
		'$route.params.blog': function(){
			if(this.$route.name.startsWith('post')) {
				this.reload_all_posts();
			}
		},
		selected_posts: function(){
			if(this.is_select_one_post) {
				this.$router.push({ name: 'post-detail', params: {blog: this.blog_pk, post: this.selected_posts[0].pk }})
			}
		},
	},
	methods: {
		reload_all_posts: function(){
			var self = this;
			this.BUS.load_post_list(function(data){
				self.all_posts = data;
			}, {
				blog: self.blog_pk,
			})
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
			this.BUS.create_new_post(type, this.blog_pk);
		},

		selected_change: function(data){
			this.selected_posts = data;
		},
		is_selected: function(post){
			return this.selected_posts.includes(post);
		},
		select_post: function(event, post){
			if(event.ctrlKey) {
				if(this.is_selected(post)) {
					this.selected_posts.remove(post);
				} else {
					this.selected_posts.push(post);
				}
			} else {
				this.selected_posts = [post];
			}
		},
		select_all: function() {
			if(this.is_select_all) {
				this.selected = [];
			} else {
				this.selected = this.posts;
			}
		},
	},
	created: function(){
		this.BUS.$on('post_list_changed', this.reload_all_posts);
	},
	mounted: function(){
		this.BUS.run_after(this.reload_all_posts, 'login');
	}
}
</script>

<style scoped>
.wrapper {
	height: 100%;
	flex: 1;
	padding-left: 5px;
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


.posts-list {
	height: 100%;
}
.posts-order {
	justify-content: space-between;
	flex: 0 0 1.6em;
}
ul.posts-ul {
	list-style: none;
	margin: 0;
	padding: 0;
	flex: 1;
	overflow-y: scroll;
}
ul.posts-ul li {
	height: 100px;
	border: solid 1px rgba(77, 79, 77, 0.27);
	margin-bottom: 2px;
}
.posts-ul li input {
	display: none;
}
.selected {
	background-color: #d9d9d9;
}
</style>
