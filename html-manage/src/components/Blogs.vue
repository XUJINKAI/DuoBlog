<template>
	<div class="wrapper box">
		<BlogSelector :blogs='blog_list'></BlogSelector>
		<router-view></router-view>
	</div>
</template>

<script>
import BlogSelector from './Blogs/BlogSelector'

export default {
	components: {
		BlogSelector,
	},
	data: function() {
		return {
		}
	},
	computed: {
		blog_list: function(){
			return this.BUS.blog_list;
		},
	},
}
</script>

<style scoped>
.wrapper {
	height: 100%;
	margin-top: 10px;
}
</style>
