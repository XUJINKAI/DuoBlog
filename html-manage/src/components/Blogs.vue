<template>
	<div class="blogs-list">
		<BlogNavs :blogs='blogs_list'></BlogNavs>
		<BlogList></BlogList>
	</div>
</template>

<script>
import BlogNavs from './Blogs/BlogNavs'
import BlogList from './Blogs/BlogList'

export default {
	data: function() {
		return {
		}
	},
	computed: {
		blogs_list: function(){
			return this.BUS.blogs_list;
		}
	},
	components: {
		BlogNavs,
		BlogList,
	}
}
</script>

<style scoped>
.blogs-list {
	display: flex;
	flex-direction: column;
}
</style>
