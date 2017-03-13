<template>
<div id="wrapper" class="box">
	<div v-if='blog' class="stretch">
		<p>name: <el-input v-model="blog.name"></el-input></p>
		<p>domain: <el-input type="input" v-model="blog.url"></el-input></p>
		<p>desc: <el-input type="input" v-model="blog.desc"></el-input></p>
		<p>
			<span>head_html:</span>
			<el-input type="textarea"
				v-model="blog.head_html"
				:rows='5'
				placeholder='e.g. your google domain verify code'>
			</el-input>
		</p>
		<p>
			<span>body_html:</span>
			<el-input type="textarea"
				v-model="blog.body_html"
				:rows='8'
				placeholder='e.g. your google analytics code'>
			</el-input>
		</p>
		<p>
			<span>custom_comment_html (if blog.comment_enable=true):</span>
			<el-input type="textarea" v-model="blog.custom_comment_html"></el-input>
		</p>
		<el-button type='success' @click='save_blog'>Save</el-button>
		<p>Danger Zone</p>
		<el-button type='danger'  @click='delete_blog'>Delete this Blog</el-button>
	</div>
	<div class="stretch">
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
				self.BUS.set_content(data, self.save_blog);
			})
		},
		delete_blog: function(){
			this.BUS.delete_blog(this.blog);
			this.BUS.clear_content();
		},
		save_blog: function(){
			var self = this;
			this.BUS.save_blog(this.blog, function(data){
				self.BUS.set_content(data, self.save_blog);
			});
		},
	},
	watch: {
		'$route': function(){
			this.reload_blog();
		},
	},
	created: function(){
		this.reload_blog();
	}
}
</script>

<style scoped>
#wrapper {
	overflow-y: auto;
	/*margin-left: 20px;*/
}
</style>