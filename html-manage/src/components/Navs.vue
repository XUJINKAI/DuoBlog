<template>
	<div class="navs stretch box y-center">
		<div>
			<a href="javascript: window.location='/manage/'" class="logo">Manager</a>
			<router-link to='/'>Blogs</router-link>
		</div>
		<span style="margin-right: 20px;">
			<a><i class="fa fa-user-circle-o" aria-hidden="true"></i> USERNAME</a>
		</span>
	</div>
</template>

<script>
export default {
	
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