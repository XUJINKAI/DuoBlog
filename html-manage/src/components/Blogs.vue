<template>
	<div class="wrapper box">
		<BlogSelector :blogs='blog_list'></BlogSelector>
		<PostsPanel></PostsPanel>
	</div>
</template>

<script>
import BlogSelector from './Blogs/BlogSelector'
import PostsPanel from './Blogs/PostsPanel'

export default {
	data: function() {
		return {
		}
	},
	computed: {
		blog_list: function(){
			return this.BUS.blog_list;
		}
	},
	components: {
		BlogSelector,
		PostsPanel,
	}
}
</script>

<style scoped>
.wrapper {
	height: 100%;
	margin-top: 10px;
}
</style>
