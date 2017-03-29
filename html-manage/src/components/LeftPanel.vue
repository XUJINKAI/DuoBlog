<template>
	<div id="wrapper">
		<div id="top">
			<BlogItem v-for='blog in blogs' :blog='blog' :key='blog.pk'></BlogItem>
		</div>
		<div id="bottom">
			<el-button @click='create' size='small'>新建博客</el-button>
			<router-link :to="{ name: 'setting' }" class="setting" :active-class="'setting_actived'" :tag="'span'"><i class="fa fa-cog" aria-hidden="true"></i> Settings</router-link>
		</div>
	</div>
</template>

<script>
import BlogItem from './LeftPanel/BlogItem'
export default {
	data: function() {
		return {
			view: 'posts'
		}
	},
	computed: {
		blogs: function(){
			return this.BUS.blog_list;
		}
	},
	components: {
		BlogItem
	},
	methods: {
		click: function(){
		},
		create: function(){
			this.BUS.create_new_blog();
		}
	}
}
</script>

<style scoped>
#wrapper {
	flex: 0 0 140px;
	display: flex;
	flex-direction: column;
	justify-content: space-between;
	height: 100%;
	overflow: hidden;
	padding-right: 15px;
	border-right: dashed 1px;
}
#top {
	flex: 1;
	overflow-y: auto;
}
#bottom {
	flex: 0 0 70px;
	margin-top: 20px;
	border-top: dashed 1px;
	display: flex;
	flex-direction: column;
	justify-content: space-around;
}
.setting {
	cursor: pointer;
}
.setting_actived {
	background: rgba(135, 138, 142, 0.23);
}
</style>
