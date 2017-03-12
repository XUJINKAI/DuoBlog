<template>
	<div id="wrapper" class="note-posts-container box stretch full-height">
		<div class="posts-filter stretch full-height">
			<Tags :tags='tags'></Tags>
		</div>
		<div class="posts-list stretch box-col">
			<div class="new-post box">
				<span>New: </span>
				<button class="stretch" v-on:click='new_markdown'>Markdown</button>
				<button class="stretch" v-on:click='new_html'>HTML</button>
			</div>
			<PostsList class='stretch' :posts='posts' @select_changed='selected_posts_change'></PostsList>
		</div>
		<div class="posts-detail stretch">
			<router-view></router-view>
		</div>
	</div>
</template>

<script>
import Tags from './PostsPanel/Tags'
import PostsList from './PostsPanel/List'
import PostEditor from './PostsPanel/PostEditor'

export default {
	components: {
		Tags,
		PostsList,
		PostEditor,
	},
	data: function(){
		return {
			all_posts: [],
			selected_tags: [],
			order_by: 'create',
			order_asc: false,
		};
	},
	computed: {
		blog_pk: function() {
			return this.$route.params.blog;
		},
		posts: function(){
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
		blog: function(){
			return this.BUS.current_blog;
		},
		selected_post: function(){
			return this.BUS.current_post;
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
		select_one_post: function(){
			return true;
		},
		select_multi_post: function(){
			return false;
		},
	},
	watch: {
		'$route': function(){
			this.reload_all_posts();
		}
	},
	created: function(){
		this.reload_all_posts();
	},
	methods: {
		reload_all_posts: function(){
			var self = this;
			API.post_list({
				blog: self.blog_pk,
				status: self.$route.meta.status,
			}, function(data){
				self.all_posts = data;
			})
		},
		create_new_post: function(type) {
			this.BUS.create_new_post(type);
		},
		select_post: function(post){
			this.BUS.select_post(post);
		},
		new_markdown: function(){
			this.BUS.create_new_post('m');
		},
		new_html: function(){
			this.BUS.create_new_post('h');
		},
		selected_posts_change: function(posts){
			if(posts.length == 1) {
				this.BUS.select_post(posts[0]);
			} else {
				this.BUS.select_post = [];
			}
		},
	},
}
</script>

<style scoped>
#wrapper {
	height: 100%;
	flex: 1;
	padding-left: 5px;
}
.note-posts-container .posts-filter {
	height: 100%;
	flex: 0 0 150px;
}
.note-posts-container .new-post {
	flex: 0 0 34px;
}
.note-posts-container .new-post button {
	flex: 1;
	margin-bottom: 10px;
}
.note-posts-container .posts-list {
	height: 100%;
	flex: 0 0 200px;
}
.note-posts-container .posts-detail {
	height: 100%;
	width: 100%;
	padding: 0 0 0 20px;
	flex: 1;
}
</style>
