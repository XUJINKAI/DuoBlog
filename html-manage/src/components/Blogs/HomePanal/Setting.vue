<template>
<div id="wrapper" class="box">
	<div v-if='blog' class="stretch left">
		<p>name: <el-input v-model="blog.name"></el-input></p>
		<p>domain: <el-input type="input" v-model="blog.domain"></el-input></p>
		<p>Absolute Url: <el-input type="input" v-model="blog.absolute_url"></el-input></p>
		<p>desc: <el-input type="input" v-model="blog.desc"></el-input></p>
		<p>
			<span>Theme:</span>
			<el-select v-model="blog.theme" placeholder="">
				<el-option label="Default" value="default"></el-option>
			</el-select>
		</p>
		<p>
			<span>head_html:</span>
			<el-input type="textarea"
				v-model="blog.head_html"
				:rows='6'
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
			<span>Comment:</span>
			<el-select v-model="blog.comments" placeholder="">
				<el-option label="Anyone" value="a"></el-option>
				<el-option label="Login" value="l"></el-option>
				<el-option label="Close" value="x"></el-option>
				<el-option label="Custom" value="c"></el-option>
			</el-select>
		</p>
		<p>
			<span>Custom Comment HTML</span>
			<el-input
				type="textarea"
				:rows='6'
				v-model="blog.custom_comment_html">
			</el-input>
		</p>
		<p>
			<span>RSS</span>
			<el-switch
				v-model="blog.rss"
				@change='save'
				on-text="on"
				off-text="off">
			</el-switch>
			<span>Sitemap</span>
			<el-switch
				v-model="blog.sitemap"
				@change='save'
				on-text="on"
				off-text="off">
			</el-switch>
		</p>
	</div>
	<div class="right stretch">
		<el-button type='success' @click='save_blog'>Save</el-button>
		<el-button type='danger'  @click='delete_blog'>Delete this Blog</el-button>
		<hr>
		<NavItem :model='navs'></NavItem>
	</div>
</div>
</template>

<script>
import NavItem from './NavItem'
export default {
	components: {
		NavItem,
	},
	data: function(){
		return {
			blog: null,
			navs: null,
		}
	},
	watch: {
		navs: {
			handler: function(val, oldVal){
				log('nav');
				// this.update_navs_to_json();
			},
			deep: true,
		}
	},
	computed: {
		blog_pk: function() {
			return this.$route.params.blog;
		},
	},
	methods: {
		parse_navs: function(json){
			if(json!=='') {
				this.navs = {name: 'root', sub: JSON.parse(json)}
			}
			else {
				this.navs = {name: 'root', sub: []}
			}
		},
		update_navs_to_json: function(){
			this.blog.navs = JSON.stringify(this.navs.sub);
		},
		reload_blog: function(){
			var self = this;
			this.BUS.load_blog(this.blog_pk, function(data){
				self.blog = data;
				self.parse_navs(data.navs);
				self.BUS.set_content(data, self.save_blog);
			})
		},
		delete_blog: function(){
			this.BUS.delete_blog(this.blog);
			this.BUS.clear_content();
		},
		save: function(){
			this.save_blog();
		},
		save_blog: function(){
			var self = this;
			this.update_navs_to_json();
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
.left {
	flex: 0 0 50%;
}
.right {
	margin-top: 30px;
	margin-left: 40px;
}
</style>