<template>
	<div id='wrapper' v-if='post' class="box-col">
		<div id="meta-div" class="box">
			<div class="stretch box-col">
				<input id="title" type="input" v-model='post.title' class='border0' placeholder="<title>">
				<div id="url" class="box">
					<strong><a :href="post.html_url" target="_blank">URL</a></strong>
					<span>: /p/</span>
					<input type="text" v-model='post.slug' class="border0 stretch" placeholder="<auto>" style='width: 30em;'/>
				</div>
				<div id="tags" class="stretch">
					<strong>Tags: </strong>
					<span v-for='tag in post.tags'>{{ tag }} <i class="fa fa-times" aria-hidden="true"></i>, </span>
					<input type="text" name="" placeholder="Add Tag" class="border0" style="width: 10em;">
				</div>
			</div>
			<div id="save-div">
				<el-button v-on:click='save_publish' type='primary'>publish</el-button>
				<el-button v-on:click='save_draft' type='success'>draft</el-button>
				<el-button v-on:click='delete_post' type='danger'>delete</el-button>
			</div>
			<div style="flex: 0 1 200px">
				<p>创建 {{ create_time }}</p>
				<p>修改 {{ last_modified_time }}</p>
				<p>
					<input type="checkbox" v-model='post.comments'>
					<span v-on:click='post.comments=!post.comments'>Comments</span>
					<input type="checkbox" v-model='post.sticky'>
					<span v-on:click='post.sticky=!post.sticky'>Sticky</span>
				</p>
			</div>
		</div>
		<HtmlEditor v-if='post.content_type == "h"' :model='post' class='editor'></HtmlEditor>
		<MdEditor v-else-if='post.content_type == "m"' :model='post' class='editor'></MdEditor>
		<p v-else>Error Type.</p>
	</div>
	<div v-else>No Data.</div>
</template>

<script>
import HtmlEditor from '@/components/Editor/HtmlEditor'
import MdEditor from '@/components/Editor/MdEditor'

export default {
	components: {
		HtmlEditor,
		MdEditor,
	},
	data: function(){
		return {
			post: null,
		};
	},
	computed: {
		url_pk: function(){
			return this.$route.params.post;
		},
		create_time: function(){
			return moment(this.post.create_time).format(this.BUS.time_format);
		},
		last_modified_time: function(){
			return moment(this.post.last_modified_time).format(this.BUS.time_format);
		},
	},
	watch: {
		'$route': function(){
			this.reload();
		},
		post: {
			handler: function(){
				log('PostEditor: post changed');
				log(JSON.stringify(this.post));
			},
			deep: true,
		},
	},
	methods: {
		reload: function(){
			var self = this;
			this.BUS.load_post(self.url_pk, function(data){
				self.post = data;
				self.BUS.set_content(data, self._save, false);
			})
		},
		delete_post: function() {
			this.BUS.delete_post(this.post);
			this.BUS.clear_content();
		},
		_save: function(){
			var self = this;
			this.BUS.save_post(this.post, function(data){
				self.BUS.set_content(data, self._save, false);
			});
		},
		save_publish: function() {
			this.post.status = 'p';
			this._save();
		},
		save_draft: function() {
			this.post.status = 'd';
			this._save();
		},
	},
	created: function() {
		var self = this;
		self.reload();
		self.BUS.$on('post_deleted', function(){
			self.post = null;
		})
	},
};
</script>

<style scoped>
#wrapper {
	height: 100%;
}
#meta-div {
	margin-bottom: 15px;
}
#title {
    font-size: x-large;
    font-weight: bolder;
}
#url, #tags {
	margin-top: 10px;
}
.editor {
	height: 100%;
}
.PostEditor-component {
	flex: 1;
	overflow: overlay;
	margin-top: 1.2em;
}
#save-div {
	flex: 0 0 60px;
	margin-right: 20px;
}
#save-div button.el-button {
	width: 100%;
	height: 32px;
	margin-left: 0;
	border-radius: 0;
}
</style>