<template>
	<div id="wrapper" class="note-posts-container box stretch full-height">
		<div class="posts-filter stretch full-height">
			<li>All</li>
			<li>sticky</li>
			<li>public</li>
			<li>hidden</li>
			<li>private</li>
			<Tags :tags='tags'></Tags>
		</div>
		<div class="posts-list stretch box-col">
			<div class="new-post box">
				<button class="stretch" @click='new_markdown'>Markdown</button>
				<button class="stretch" @click='new_html'>HTML</button>
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
	methods: {
		reload_all_posts: function(){
			var self = this;
			this.BUS.load_post_list(function(data){
				self.all_posts = data;
			}, {
				blog: self.blog_pk,
			})
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
		selected_posts_change: function(posts){
			if(posts.length == 1) {
				this.BUS.select_post(posts[0]);
			} else {
				this.BUS.select_post = [];
			}
		},
	},
	created: function(){
		this.BUS.$on('post_list_changed', this.reload_all_posts);
	},
	mounted: function(){
		this.reload_all_posts();
	}
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
