<template>
	<div id="app">
		<Navs></Navs>
		<router-view></router-view>
	</div>
</template>

<script>
import Navs from '@/components/Navs'
export default {
	name: 'app',
	components: {
		Navs
	}
}
</script>

<style>
body {
	overflow: hidden;
	position: absolute;
	bottom: 0;
	left: 0;
	right: 0;
	top: 0;
}
#app {
	font-family: 'Avenir', Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	color: #2c3e50;
	margin: 0;
	padding: 10px;
	display: flex;
	flex-direction: column;
	position: absolute;
	left: 0;
	right: 0;
	top: 0;
	bottom: 0;
}

/* common */
.box {
	display: flex;
}
.box-col {
	display: flex;
	flex-direction: column;
}
.y-scroll {
	overflow-y: auto;
}
.y-center {
	align-items: center;
}
.stretch {
	flex-grow: 1;
}
.full-height {
	height: 100%;
}
.bolder {
	font-weight: bolder;
}
.border0 {
	border: 0;
}
.margin0 {
	margin: 0;
}
.padding {
	padding: 0;
}
</style>
