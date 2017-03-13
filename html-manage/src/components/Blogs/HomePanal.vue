<template>
<div id="wrapper">
	<div>
		<router-link :to="{name: 'blog'}">Setting</router-link>
		<router-link :to="{name: 'blog-navs'}">Navs</router-link>
		<router-link :to="{name: 'blog-import-jekyll'}">ImportJekyll</router-link>
	</div>
	<div id="content">
		<router-view></router-view>
	</div>
</div>
</template>

<script>
export default {
}
</script>

<style scoped>
#wrapper {
	overflow: auto;
	margin-top: 5px;
	margin-left: 20px;
	width: calc(100% - 20px);
}
#content {
	width: 100%;
}
</style>