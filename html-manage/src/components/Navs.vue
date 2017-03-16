<template>
	<div class="navs stretch box y-center">
		<span id="left" class="box">
			<a href="javascript: window.location='/manage/'" class="logo">Manager</a>
			<ul class="box">
				<li v-for='blog in blogs' v-if='blog.absolute_url'><a :href='blog.absolute_url'>
					<i class="fa fa-home" aria-hidden="true"></i>
					{{ blog.name }}
				</a></li>
			</ul>
		</span>
		<span id="right" class="box">
			<a href="/admin" target="_blank"><i class="fa fa-wrench" aria-hidden="true"></i> Dj-Admin</a>
			<router-link :to="{name: 'userme'}" tag='a' :active-class="'active-nav'">
				<i class="fa fa-user-circle-o" aria-hidden="true"></i> {{ username }}
			</router-link>
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
			return this.BUS.username;
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
	color: black;
	font-style: italic;
}
.active-nav {
	font-weight: bold;
}
#left,
#right {
	align-items: baseline;
}
#left ul {
	list-style: none;
	margin-left: 0px;
	padding-left: 10px;
}
#left ul li {
	margin-left: 15px;
}
#right {
	/*margin-right: 20px;*/
}
#right ul {
	list-style: none;
	margin-right: 5px;
}
#right ul li {
	/*margin-right: 20px;*/
}
#right a {
	margin-right: 20px;
}
ul li:hover {
	cursor: pointer;
}
.logo, li, a {
	text-decoration: none;
}
a, a:visited, a:active, a:focus {
	color: black;
}
</style>