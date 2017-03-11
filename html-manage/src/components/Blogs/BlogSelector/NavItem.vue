<template>
<div class="wrapper">
	<div>
		<span v-on:click='btn_click("setting")' :class="{blog_title_clicked: btn_clicked('setting')}" class="blog_title">{{ blog.name }}</span>
		<a :href="'//' + blog.url" target="_blank" style="margin-left: 10px;"><i class="fa fa-external-link" aria-hidden="true"></i></a>
	</div>
	<ul class="blog_btn_ul">
		<li v-on:click='btn_click("posts")' :class="{blog_btn_clicked: btn_clicked('posts')}" class="blot_btn">博文 ({{ blog.post_count }})</li>
		<li v-on:click='btn_click("draft")' :class="{blog_btn_clicked: btn_clicked('draft')}" class="blot_btn">草稿 ({{ blog.draft_count }})</li>
		<li v-on:click='btn_click("trash")' :class="{blog_btn_clicked: btn_clicked('trash')}" class="blot_btn">废纸篓({{ blog.trash_count }})</li>
		<li v-on:click='btn_click("comment")' :class="{blog_btn_clicked: btn_clicked('comment')}" class="blot_btn">评论 ({{ blog.comment_count }})</li>
		<li v-on:click='btn_click("navs")' :class="{blog_btn_clicked: btn_clicked('navs')}" class="blot_btn">导航</li>
	</ul>
</div>
</template>

<script>
export default {
	props: {
		blog: Object
	},
	computed: {
		blogs: function(){
			return this.BUS.blog_list;
		},
	},
	methods: {
		btn_click: function(name){
			this.BUS.select_blog_function(this.blog, name);
		},
		btn_clicked: function(name){
			return this.BUS.current_blog==this.blog&&this.BUS.current_blog_btn==name;
		},
	},
}
</script>

<style scoped>
.wrapper {
	margin-bottom: 10px;
}
.blog_title {
	font-size: 1.1em;
    font-weight: bolder;
    text-decoration: underline;
}
.blog_title:hover,
.blot_btn:hover {
	cursor: pointer;
}
.blog_title_clicked,
.blog_btn_clicked {
	background-color: rgba(135, 138, 142, 0.23);
}
.blog_btn_ul {
	list-style-type: none;
	margin: 0;
    padding: 0;
}
.blog_btn_ul li {
	padding-left: 20px;
}
</style>