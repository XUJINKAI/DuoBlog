<template>
<div>
	<a @click='logout'>Logout</a>
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