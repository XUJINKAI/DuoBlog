<template>
	<div id='wrapper' v-if='post' class="box-col">
		<div id="meta-div" class="box">
			<div class="stretch">
				<input id="title" type="input" v-model='post.title' class='border0' style="width: 90%;" placeholder="<title>">
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
				<p style="margin-top: 10px; color: gray;">创建 {{ create_time }}, 修改({{post.modified_count}}) {{ last_modified_time }}</p>
			</div>
			<div id="save-div">
				<el-button @click='save_publish' type='primary' :class="{active_status: post.status=='p'}">Publish</el-button>
				<el-button @click='save_draft' type='success' :class="{active_status: post.status=='d'}">Draft</el-button>
				<el-button @click='delete_post' type='danger' :class="{active_status: post.status=='t'}">Delete</el-button>
			</div>
			<div style="info-div">
				<el-select v-model="post.blog" placeholder="">
					<el-option
						v-for="blog in BUS.blog_list"
						:key='blog.pk'
						:label="blog.name"
						:value="blog.pk">
					</el-option>
				</el-select>
				<p class="cs_switch">
					<span>Comments</span>
					<el-switch
						v-model="post.comments"
						@change='save'
						on-text="on"
						off-text="off">
					</el-switch>
				</p>
				<p class="cs_switch">
					<span>Sticky</span>
					<el-switch
						v-model="post.sticky"
						@change='save'
						on-text="on"
						off-text="off">
					</el-switch>
				</p>
			</div>
		</div>
		<MdEditor
			v-if='post.content_type == "m"'
			:model='post'
			@save='save'
			class='editor'>
		</MdEditor>
		<HtmlEditor
			v-else-if='post.content_type == "h"'
			:model='post'
			class='editor'
			></HtmlEditor>
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
			// 传说中的回调地狱？
			self.BUS.suppress_router(function(release_suppress){
				self.BUS.save_post(self.post, function(data){
					release_suppress(function(){
						// data didn't contains these fields
						self.post.last_modified_time = Date();
						self.post.modified_count += 1;
						self.BUS.set_content(self.post, self._save, false);
					});
				});
			})
		},
		save: function(){
			this._save();
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
.active_status,
.active_status:visited,
.active_status:focus
 {
	color: black;
	text-decoration: underline;
}
.editor {
	flex: 1;
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
#info-div {
	flex: 0 1 200px
}
.cs_switch {
	display: flex;
}
.cs_switch span {
	flex: 0 0 90px;
}
</style>