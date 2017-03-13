<template>
	<div id="app" class="layout">
		<Navs></Navs>
		<router-view></router-view>
		<Login v-if='Modal_Login' @login='on_login'></Login>
		<SaveNoCancel v-if='Modal_SaveNoCancel' @close='Modal_SaveNoCancel_Close'></SaveNoCancel>
		<BlogDelete v-if='Model_BlogDelete' @close='Model_BlogDelete_Close'></BlogDelete>
	</div>
</template>

<script>
import Navs from '@/components/Navs'
import Login from '@/components/prompt/login'
import SaveNoCancel from '@/components/prompt/save_no_cancel'
import BlogDelete from '@/components/prompt/blog_delete'

export default {
	name: 'app',
	components: {
		Navs,
		Login,
		SaveNoCancel,
		BlogDelete,
	},
	data: function() {
		return {
			Modal_SaveNoCancel: false,
			Modal_SaveNoCancel_Resolve: null,

			Model_BlogDelete: false,
			Model_BlogDelete_Resolve: null,
		}
	},
	computed: {
		Modal_Login: function(){
			return !this.BUS.is_login;
		}
	},
	methods: {
		on_login: function(username, password){
			this.BUS.login(username, password);
		},

		Modal_SaveNoCancel_Close: function(result){
			this.Modal_SaveNoCancel = false;
			this.Modal_SaveNoCancel_Resolve(result);
		},
		save_no_cancel: function(callback){
			this.Modal_SaveNoCancel_Resolve = callback;
			this.Modal_SaveNoCancel = true;
		},

		Model_BlogDelete_Close: function(result){
			this.Model_BlogDelete = false;
			this.Model_BlogDelete_Resolve(result);
		},
		blog_delete: function(callback){
			this.Model_BlogDelete_Resolve = callback;
			this.Model_BlogDelete = true;
		},
	},
	created: function() {
		this.BUS.modal_save_no_cancel = this.save_no_cancel;
		this.BUS.modal_blog_delete = this.blog_delete;
	}
}
</script>

<style>
body {
	font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
	font-size: 14px;
	line-height: 1.5;
	overflow: hidden;
	position: absolute;
	bottom: 0;
	left: 0;
	right: 0;
	top: 0;
}
#app {
	color: #2c3e50;
	margin: 0;
	padding: 0;
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
	display: -webkit-box;
	display: flex;
}
.box-col {
	display: -webkit-box;
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
