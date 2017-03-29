<template>
<div>
	<p>Author: <a href="https://github.com/XUJINKAI" target="_blank">XUJINKAI</a></p>
	<p>Version: -{{ version }}</p>
	<button @click='update'>update</button>
</div>
</template>

<script>
export default {
	data () {
		return {
		}
	},
	computed: {
		version(){
			return this.BUS.version;
		}
	},
	methods: {
		update() {
			this.BUS.system_update();
		}
	},
}
</script>