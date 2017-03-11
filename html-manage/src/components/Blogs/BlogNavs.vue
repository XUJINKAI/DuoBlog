<template>
	<div>
		<BlogNavsItem v-for='blog in blogs' :blog='blog'></BlogNavsItem>
	</div>
</template>

<script>
import BlogNavsItem from './Blognavs/BlogNavsItem'
export default {
	data: function() {
		return {
			view: 'posts'
		}
	},
	props: {
		blogs: Object,
	},
	components: {
		BlogNavsItem
	},
	methods: {
		click: function(){
		}
	}
}
</script>

<style scoped>
</style>
