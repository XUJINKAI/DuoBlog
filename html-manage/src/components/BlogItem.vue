<template>
	<div>
		<p @click='click'>{{ blog.name }}</p>
		<router-link to='/blog/setting'></router-link>
	</div>
</template>

<script>
export default {
	data: function() {
		return {
			view: 'posts'
		}
	},
	props: {
		blog: Object,
	},
	methods: {
		click: function(){
		}
	}
}
</script>

<style scoped>
</style>
