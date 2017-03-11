<template>
	<div id="wrapper">
		<NavItem v-for='blog in blogs' :blog='blog' :key='blog.pk'></NavItem>
		<span @click='create'>新建</span>
	</div>
</template>

<script>
import NavItem from './BlogSelector/NavItem'
export default {
	data: function() {
		return {
			view: 'posts'
		}
	},
	props: {
		blogs: Array,
	},
	components: {
		NavItem
	},
	methods: {
		click: function(){
		},
		create: function(){
			this.BUS.create_new_blog();
		}
	}
}
</script>

<style scoped>
#wrapper {
	flex: 0 0 180px;
	height: 100%;
	overflow: auto;
	padding-right: 15px;
	border-right: dashed 1px;
}
</style>
