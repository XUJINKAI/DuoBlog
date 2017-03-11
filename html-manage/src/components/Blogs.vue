<template>
	<div class="blogs-list">
		<BlogItem v-for='blog in blogs_list' :blog='blog' :key='blog.pk'></BlogItem>
		<router-view></router-view>
		<p>
			Blogs {{ $route.params.pk }} {{ $route.params }}
		</p>
	</div>
</template>

<script>
import BlogItem from './BlogItem'

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
		BlogItem
	}
}
</script>

<style scoped>
.blogs-list {
	display: flex;
	flex-direction: column;
}
</style>
