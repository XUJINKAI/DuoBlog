<template>
<div id="wrapper" class="box">
	<div id="left" v-if='blog'>
		name: <input id="pk" type="input" v-model="blog.name"></p>
		domain: <input id="pk" type="input" v-model="blog.url"></p>
		desc: <input id="pk" type="input" v-model="blog.desc"></p>
		head_html: <input id="pk" type="input" v-model="blog.head_html"></p>
		body_html: <input id="pk" type="input" v-model="blog.body_html"></p>
		custom_comment_html: <input id="pk" type="input" v-model="blog.custom_comment_html"></p>
	</div>
	<div id="right">
		<a @click='save_blog'>Save</a>
		<a @click='delete_blog'>Delete</a>
	</div>
</div>
</template>

<script>
export default {
	data: function(){
		return {
			raw_blog: null,
			blog: null,
		}
	},
	computed: {
		blog_pk: function() {
			return this.$route.params.blog;
		}
	},
	methods: {
		reload_blog: function(){
			var self = this;
			API.blog_detail(this.blog_pk, function(data){
				self.blog = data;
				self.raw_blog = JSON.parse(JSON.stringify(data));
				self.BUS.content_changed = false;
			})
		},
		delete_blog: function(){
			this.BUS.content_changed = false;
			this.BUS.delete_blog(this.blog);
		},
		save_blog: function(){
			var self = this;
			this.BUS.save_blog(this.blog, function(){
				self.BUS.content_changed = false;
			});
		},
	},
	watch: {
		'$route': function(){
			this.reload_blog();
		},
		blog: {
			handler: function(val, oldVal){
				this.BUS.content_changed = (JSON.stringify(this.blog)!==JSON.stringify(this.raw_blog));
			},
			deep: true,
		},
	},
	created: function(){
		this.reload_blog();
	}
}
</script>

<style scoped>
#wrapper {
	margin-left: 20px;
}
</style>