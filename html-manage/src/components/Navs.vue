<template>
	<div class="navs stretch box y-center">
		<span id="left" class="box">
			<a href="javascript: window.location='/manage/'" class="logo">Manager</a>
			<ul class="box">
				<router-link :to="{ name: 'blog'}" :tag="'li'" :active-class="'active-nav'">Blogs</router-link>
			</ul>
		</span>
		<span id="right" class="box">
			<ul class="box">
				<li v-for='blog in blogs'><a :href='"//" + blog.url' target="_blank">
					<i class="fa fa-home" aria-hidden="true"></i>
					{{ blog.name }}
				</a></li>
			</ul>
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
			return '//XJK';
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
	font-size: 14px;
	font-weight: bolder;
	color: black;
}
.active-nav {
	font-weight: bold;
	text-decoration: underline;
}
#left {
	align-items: baseline;
}
#left ul {
	list-style: none;
	margin-left: 10px;
}
#left ul li {
	margin-left: 10px;
}
#right {
	margin-right: 20px;
}
#right ul {
	list-style: none;
	margin-right: 5px;
}
#right ul li {
	margin-right: 20px;
}
ul li:hover {
	cursor: pointer;
}
</style>