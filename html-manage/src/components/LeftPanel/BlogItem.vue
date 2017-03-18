<template>
<div class="wrapper">
	<div>
		<router-link :to="{ name: 'blog', params: {blog: blog.pk } }" class="blog_title" :active-class="'blog_title_actived'" :tag="'li'" exact>{{ blog.name }}</router-link>
	</div>
	<ul class="blog_btn_ul">
		<router-link :to="{ name: 'post-list', params: { blog: blog.pk } }" class="blog_btn" :active-class="'blog_btn_clicked'" :tag="'li'">博文 ({{ blog.post_count }})</router-link>
		<router-link :to="{ name: 'trash', params: {blog: blog.pk } }" class='blog_btn' :active-class="'blog_btn_clicked'" :tag="'li'">废纸篓 ({{ blog.trash_count }})</router-link>
		<!-- <li>评论 ({{ blog.comment_count }})</li> -->
	</ul>
</div>
</template>

<script>
export default {
	props: {
		blog: Object
	},
}
</script>

<style scoped>
.wrapper {
	margin-bottom: 10px;
}
.blog_title {
	display: inline-block;
	width: 100%;
	font-size: 1.1em;
    font-weight: bolder;
    text-decoration: underline;
}
.blog_title:hover,
.blog_btn:hover {
	cursor: pointer;
}
.blog_title_actived {
	background-color: rgba(135, 138, 142, 0.4);
}
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