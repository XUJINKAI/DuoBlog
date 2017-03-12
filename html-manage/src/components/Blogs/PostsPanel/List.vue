<template>
<div class="post-list-container box-col">
	<div class="post-order box" style="justify-content: space-between;">
		<input type="checkbox" v-on:click='select_all' :bind='is_select_all'>
		<span :class='{bolder: order_by=="title"}'>Title <span v-if='order_by=="title"'>{{ order_asc?'↑':'↓'}}</span></span>
		<span :class='{bolder: order_by=="create"}'>Create <span v-if='order_by=="create"'>{{ order_asc?'↑':'↓'}}</span></span>
		<span :class='{bolder: order_by=="modify"}'>Modify <span v-if='order_by=="modify"'>{{ order_asc?'↑':'↓'}}</span></span>
	</div>
	<ul class="post-list">
		<router-link
			v-for='post in posts' :key='post.pk'
			:to="{ name: status2view(post.status), params: {blog: blog_pk, post: post.pk }}"
			class="post-item"
			:active-class="'selected_post'"
			:tag="'li'"
			>
			<input type="checkbox" value='post' v-model='selected_posts'>
			<p>{{ post.title }}</p>
			<!-- <span>{{ post.last_modified_time }}</span> -->
		</router-link>
	</ul>
</div>
</template>

<script>
export default {
	data: function(){
		return {
			selected_posts: [],
			order_by: 'create',
			order_asc: false,
		}
	},
	props: {
		posts: Array,
	},
	computed: {
		blog_pk: function(){
			return this.$route.params.blog;
		},
		is_select_all: function(){
			return this.posts.every(this.is_selected);
		},
	},
	methods: {
		status2view: function(status){
			var map = {
				'p': 'post-detail',
				'd': 'draft-detail',
				't': 'trash-detail',
			}
			return map[status];
		},
		is_selected: function(post){
			return this.selected_posts.includes(post);
		},
		select_all: function() {
			if(this.is_select_all) {
				this.selected_posts = [];
			} else {
				this.selected_posts = this.posts;
			}
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
			this.selected_changed();
		},
	}
};
</script>

<style>
.post-list-container {
	height: 100%;
}
.post-list-container .post-order {
	flex: 0 0 1.6em;
}
.post-list-container .post-list {
	flex: 1;
	overflow-y: scroll;
}
.post-list-container ul.post-list {
	list-style: none;
	margin: 0;
	padding: 0;
}
.post-list-container ul.post-list li {
	height: 100px;
	border: solid 1px rgba(77, 79, 77, 0.27);
	margin-bottom: 2px;
}
.post-list-container .selected_post {
	background-color: #d9d9d9;
}
.post-list-container .post-list li input {
	display: none;
}
</style>