<template>
<div id="wrapper">
	<div id="left">
		<div id="operator">
			<button @click='restore_posts'>Restore</button>
			<button @click='delete_posts'>Delete</button>
			<button @click='delete_all_posts'>Delete All Trash</button>
		</div>
		<table id="list">
			<thead>
				<tr>
					<th><input type="checkbox" @click='check_all' v-model='is_selected_all'/>{{selected_list.length}}</th>
					<th>Title</th>
					<th>Abstract</th>
					<th>Tags</th>
					<th>Comments</th>
					<th>Status</th>
					<th>Views</th>
					<th>Modified</th>
					<th>Create</th>
					<th>Modified</th>
				</tr>
			</thead>
			<tr v-for='post in posts' :key='post.pk'>
				<th><input type="checkbox" :value='post' v-model='selected_list'/></th>
				<th @click='selected_list=[post]'>{{ post.title }}</th>
				<th @click='selected_list=[post]'>{{ post.abstract }}</th>
				<th></th> 
				<th>{{ post.comments }}</th>
				<th>{{ post.status | status_filter }}</th>
				<th>{{ post.views_count }}</th>
				<th>{{ post.modified_count }}</th>
				<th>{{ post.create_time | fromNow }}</th>
				<th>{{ post.last_modified_time | fromNow }}</th>
			</tr>
		</table>
	</div>
	<div id="right">
		Preview:
		<div v-if='post'>
			<div>{{ post.title }}</div>
			<div v-html='post.rendered_html'></div>
		</div>
	</div>
</div>
</template>

<script>
export default {
	data: function(){
		return {
			posts: [],
			selected_list: [],
			post: null,
		}
	},
	computed: {
		blog_pk: function() {
			return this.$route.params.blog;
		},
		is_selected_all: function(){
			return this.posts.length == this.selected_list.length;
		},
		is_selected_one: function(){
			return this.selected_list.length == 1;
		},
	},
	watch: {
		'$route': function(){
			if(this.$route.name=='trash') {
				this.load_data();
			}
		},
		selected_list: {
			handler: function(){
				if(this.is_selected_one) {
					var pk = this.selected_list[0].pk;
					var self = this;
					this.BUS.load_post(pk, function(data){
						self.post = data;
					})
				} else {
					this.post = null;
				}
			},
			deep: true
		}
	},
	methods: {
		load_data: function(){
			var self = this;
			this.BUS.load_post_list({
				blog: self.blog_pk,
				deleted: true,
			}, function(data){
				self.posts = data;
			})
		},
		check_all: function(){
			if(this.is_selected_all) {
				this.selected_list = [];
			} else {
				this.selected_list = this.posts;
			}
		},
		_delete_select: function(){
			var self = this;
			var delete_pks = [];
			self.selected_list.forEach(function(post){
				delete_pks.push(post.pk);
			})
			self.BUS.delete_posts_batch(delete_pks, function(){
				self.load_data();
				self.selected_list = [];
				self.BUS.reload_blog_list();
			});
		},
		delete_all_posts: function(){
			if(confirm('Delete selected permanently, are you sure ?')) {
				this.selected_list = this.posts;
				this._delete_select();
			}
		},
		delete_posts: function(){
			if(confirm('Delete selected permanently, are you sure ?')) {
				this._delete_select();
			}
		},
		restore_posts: function(){
			var self = this;
			var pks = [];
			self.selected_list.forEach(function(post){
				pks.push(post.pk);
			})
			self.BUS.restore_posts_batch(pks, function(){
				self.load_data();
				self.selected_list = [];
				self.BUS.reload_blog_list();
			});
		},
	},
	filters: {
		fromNow: function(time) {
			return moment(time).fromNow();
		},
		status_filter: function(status){
			var map = {
				's': 'Sticky',
				'p': 'Public',
				'h': 'Hidden',
				'x': 'Private',
			}
			return map[status];
		},
	},
	mounted: function(){
		this.load_data();
	}
}
</script>

<style scoped>
#wrapper {
	width: 100%;
	overflow-y: scroll;
	display: flex;

}
#left, #right {
	flex: 1;
}
#right {
	word-break: break-all;
}
#operator {

}
#list {
	width: 100%;
	overflow-y: scroll;
}
</style>