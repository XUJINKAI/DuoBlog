<template>
	<div v-if='post' class="post-detail-container box-col">
		<div class="box">
			<div class="stretch box-col">
				<input type="input" v-model='post.title' class='post_detail_title border0'></p>
				<p class="box"><strong>URL</strong><span>: /posts/</span>
					<input type="text" v-model='post.slug' class="border0 stretch" placeholder="<auto>" style='width: 30em;'/>
					<a :href="post.html_url" target="_blank">Open</a>
				</p>
				<div class="stretch">
					<strong>Tags: </strong>
					<span v-for='tag in post.tags'>{{ tag }} <i class="fa fa-times" aria-hidden="true"></i>, </span>
					<input type="text" name="" placeholder="Add Tag" class="border0" style="width: 10em;">
				</div>
			</div>
			<div style="flex: 0 1 100px">
				<button v-on:click='save_publish'>publish</button>
				<button v-on:click='save_draft'>draft</button>
				<button v-on:click='delete_current'>delete</button>
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
		<HtmlEditor v-if='post.content_type == "h"' :model='post'></HtmlEditor>
		<MdEditor v-else-if='post.content_type == "m"' :model='post'></MdEditor>
		<p v-else>Error Type.</p>
	</div>
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
		};
	},
	computed: {
		post: function(){
			return this.BUS.post_detail;
		},
		create_time: function(){
			return moment(this.post.create_time).format(this.BUS.time_format);
		},
		last_modified_time: function(){
			return moment(this.post.last_modified_time).format(this.BUS.time_format);
		},
	},
	methods: {
		reload: function(){
			this.BUS.reload_post_detail();
		},
		delete_current: function() {
			this.BUS.delete_post_detail();
		},
		save_publish: function() {
			this.BUS.save_post_detail_public();
		},
		save_draft: function() {
			this.BUS.save_post_detail_draft();
		},
	}

};
</script>

<style>
.post-detail-container {
	height: 100%;
}
.post_detail_title {
    font-size: x-large;
    font-weight: bolder;
}
.PostEditor-component {
	flex: 1;
	overflow: overlay;
	margin-top: 1.2em;
}
</style>