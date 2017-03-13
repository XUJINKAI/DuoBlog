<template>
<div id="import_jekyll_app" style="margin-top: 30px;">
	<div class="col-md-4">
		<div id="jekyll_md_holder" class="text-center">
			<p>NOT available NOW.</p>
			<p>Drag jekyll post.md files here</p>
			<p>click file name to view content</p>
		</div>
		<div style="margin: 10px 0 10px 10px;">
			<button class="btn btn-primary">Import {{select_count}} posts</button>
			to
			<select class="" id="blogs_list">
				{% for blog in blogs %}
				<option :value="blog.pk">{{ blog.name }}</option>
				{% endfor %}
			</select>
			<br>
			<button class="btn btn-default">select all</button>
			<button class="btn btn-default">reverse select</button>
		</div>
		<div style="margin: 5px;" class="file_list">
			<p>Load list:</p>
			<ul style="max-height: 300px; overflow: scroll;">
				<p v-for="file in files" :key='file.name'>
					<input type="checkbox" v-bind:checked="file.check">
					<label>{{ file.name }}</label>
				</p>
			</ul>
			<hr>
			<p>Error list:</p>
			<ul style="max-height: 500px; overflow: scroll;">
				<label v-for="file in error_files" :key='file.name' v-on:click=''>{{ file.name }}</label>
			</ul>
		</div>
	</div>
	<div class="col-md-8" v-if='current_file'>
		<p><strong>URL:</strong> {{ current_file.url }}</p>
		<p><strong>TITLE:</strong> {{ current_file.title }}</p>
		<p><strong>TAGS:</strong> {{ current_file.tags }}</p>
		<p><strong>LAST_MODIFIED_TIME:</strong> {{ current_file.last_modified_time }}</p>
		<p><strong>FILENAME:</strong> {{ current_file.name }}</p>
		<p><strong>SIZE:</strong> {{ current_file.size }}</p>
		<hr>
		<div v-html='current_marked'></div>
	</div>
</div>
</template>

<script>
export default {
	data(){
		return {
			blog: {},
			file: {},
			current_file: {},
			current_marked: {},
			error_files: {},
			files: {},
			select_count: 0,
		}
	}
}
</script>

<style>
#jekyll_md_holder {
	border: 10px dashed #ccc;
	width: 300px;
	min-height: 100px;
	margin: 0px auto;
}
#jekyll_md_holder.hover {
	border: 10px dashed #0c0;
}
#jekyll_md_holder p {
	color: #797979;
	font-size: large;
}
.file_list .btn-default {
	border-color: #FFF;
	padding: 0px;
}
</style>