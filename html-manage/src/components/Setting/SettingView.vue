<template>
<div id="wrapper">
	<div>
		<router-link :to="{name: 'setting'}">About</router-link>
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