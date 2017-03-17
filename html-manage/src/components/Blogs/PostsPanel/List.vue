<template>
<div id="wrapper" class="box-col">
	<div id="head" class="post-order box">
		<input type="checkbox" v-on:click='select_all' :bind='is_select_all'>
		<span :class='{bolder: order_by=="title"}'>Title <span v-if='order_by=="title"'>{{ order_asc?'↑':'↓'}}</span></span>
		<span :class='{bolder: order_by=="create"}'>Create <span v-if='order_by=="create"'>{{ order_asc?'↑':'↓'}}</span></span>
		<span :class='{bolder: order_by=="modify"}'>Modify <span v-if='order_by=="modify"'>{{ order_asc?'↑':'↓'}}</span></span>
	</div>
	<ul id="list" class="post-list">
		<li
			v-for='post in posts' :key='post.pk'
			class="post-item"
			:class="{selected: is_selected(post)}"
			@click='select_post($event, post)'
			>
			<input type="checkbox" value='post' v-model='selected'>
			<p>{{ post.abstract }}</p>
			<!-- <span>{{ post.last_modified_time }}</span> -->
		</li>
	</ul>
</div>
</template>

<script>
export default {
	props: {
		posts: Array,
	},
	data: function(){
		return {
			selected: [],
			order_by: 'create',
			order_asc: false,
		}
	},
	computed: {
		blog_pk: function(){
			return this.$route.params.blog;
		},
		is_select_all: function(){
			return this.posts.every(this.is_selected);
		},
	},
	watch: {
		selected: function(){
			this.$emit('selected', this.selected);
		}
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
			return this.selected.includes(post);
		},
		select_all: function() {
			if(this.is_select_all) {
				this.selected = [];
			} else {
				this.selected = this.posts;
			}
		},
		select_post: function(event, post){
			if(event.ctrlKey) {
				if(this.is_selected(post)) {
					this.selected.remove(post);
				} else {
					this.selected.push(post);
				}
			} else {
				this.selected = [post];
			}
		},
	}
};
</script>

<style>
#wrapper {
	height: 100%;
}
#head {
	justify-content: space-between;
}
.post-order {
	flex: 0 0 1.6em;
}
.post-list {
	flex: 1;
	overflow-y: scroll;
}
ul.post-list {
	list-style: none;
	margin: 0;
	padding: 0;
}
ul.post-list li {
	height: 100px;
	border: solid 1px rgba(77, 79, 77, 0.27);
	margin-bottom: 2px;
}
.selected {
	background-color: #d9d9d9;
}
.post-list li input {
	display: none;
}
</style>