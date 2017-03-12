<template>
	<div class="navs stretch box y-center">
		<div>
			<a href="javascript: window.location='/manage/'" class="logo">Manager</a>
			<router-link :to="{ name: 'blog'}">Blogs</router-link>
		</div>
		<span style="margin-right: 20px;">
			<a v-for='blog in blogs' :href='"//" + blog.url'>{{ blog.name }}</a>
			<a><i class="fa fa-user-circle-o" aria-hidden="true"></i> {{ username }}</a>
		</span>
	</div>
</template>

<script>
export default {
	computed: {
		blogs: function() {
			return this.BUS.blog_list;
		},
		username: function(){
			return 'XJK';
		}
	}
}
</script>

<style scoped>
.navs {
	flex: 0 0 32px;
	border-bottom: 1px dashed #777777;
	padding-bottom: 2px;
	justify-content: space-between;
}
.logo {
	font-weight: bolder;
	color: black;
}
</style>