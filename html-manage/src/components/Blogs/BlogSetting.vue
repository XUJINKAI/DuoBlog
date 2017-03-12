<template>
<div id="wrapper">
	pk: {{ blog_pk }}
	<a @click='delete_blog'>Delete</a>
	<div v-if='blog'>
		{{ blog.pk }}
	</div>
</div>
</template>

<script>
export default {
	data: function(){
		return {
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
			})
		},
		delete_blog: function(){
			this.BUS.delete_blog(this.blog);
		}
	},
	watch: {
		'$route': function(){
			this.reload_blog();
		}
	},
	created: function(){
		this.reload_blog();
	}
}
</script>

<style scoped>
</style>