<template>
<div>
	<a @click='logout' id="logout">Logout</a>
</div>
</template>

<script>
export default {
	methods: {
		logout: function(){
			this.BUS.logout();
		}
	}
}
</script>

<style scoped>
#logout {
	right: 0;
	position: fixed;
}
</style>