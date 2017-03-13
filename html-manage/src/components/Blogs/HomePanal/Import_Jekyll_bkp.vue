<template>
<div id="import_jekyll_app" style="margin-top: 30px;">
	<div class="col-md-4">
		<div id="jekyll_md_holder" class="text-center">
			<p>Drag jekyll post.md files here</p>
			<p>click file name to view content</p>
		</div>
		<div style="margin: 10px 0 10px 10px;">
			<button class="btn btn-primary" @click="start_import_data">Import {{select_count}} posts</button>
			to
			<select class="" id="blogs_list">
				{% for blog in blogs %}
				<option :value="blog.pk">{{ blog.name }}</option>
				{% endfor %}
			</select>
			<br>
			<button class="btn btn-default" v-on:click='select_all();'>select all</button>
			<button class="btn btn-default" v-on:click='reverse_select();'>reverse select</button>
		</div>
		<div style="margin: 5px;" class="file_list">
			<p>Load list:</p>
			<ul style="max-height: 300px; overflow: scroll;">
				<p v-for="file in files" :key='file.name'>
					<input type="checkbox" v-bind:checked="file.check" v-on:click="file_check($event, file);">
					<label v-on:click='file_preview($event, file);'>{{ file.name }}</label>
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
	data: {
		files: [],
		current_file: null,
		current_marked: '',
		error_files: [],
	},
	computed: {
		current_marked: function(){
			return marked(this.current_file.content);
		},
		select_count: function(){
			var count = 0;
			for (var i = this.files.length - 1; i >= 0; i--) {
				count += this.files[i].check
			}
			return count;
		}
	},
	methods: {
		file_check: function(event, file){
			file.check = !file.check;
		},
		file_preview: function(event, file){
			this.current_file = file;
		},
		select_all: function(){
			for (var i = this.files.length - 1; i >= 0; i--) {
				this.files[i].check = true;
			}
		},
		reverse_select: function(){
			for (var i = this.files.length - 1; i >= 0; i--) {
				this.files[i].check = !this.files[i].check;
			}
		},
		start_import_data: function(){
			var blog_pk = $("#blogs_list").val();
			for (var i = import_jekyll_app.files.length - 1; i >= 0; i--) {
				var file = import_jekyll_app.files[i];
				$.ajax({
					url: "{% url 'api:post-list' %}",
					method: 'POST',
					headers: {
						'X-CSRFToken': getCookie('csrftoken'),
					},
					dataType: 'json',
					data: {
						'title': file.title,
						'content': file.content,
						'content_type': 'm',
						'status': 'p',
						'comments': true,
						'sticky': false,
						'tags': JSON.stringify(file.tags),
					},
					success: function(data){
						import_jekyll_app.files = [];
					},
					error: function(data){
						console.log(data.responseText);
					}
				})
			}
			alert('done, see console if error happened.');
		},
		analysis_post: function(data, file){
			try{
				var title, tags, content;
				var arr = data.match(/-{3,}([\s\S]*?)-{3,}([\s\S]*)/);
				content = arr[2];
				var arr_tagstr = arr[1].match(/tags:(.*)/)
				if(arr_tagstr) {
					tags = arr_tagstr[1].match(/(?!,)(\S+)/g);
				}
				var arr_catstr = arr[1].match(/categories:(.*)/)
				if(arr_catstr) {
					cate = arr_catstr[1].match(/(?!,)(\S+)/g);
					tags.push(cate[0])
				}
				var arr_titlestr = arr[1].match(/title:(.*)/)
				if (arr_titlestr) {
					title = arr_titlestr[1];
				}
				return {
					'title': title,
					'tags': tags,
					'content': content,
				}
			} catch(e) {
				console.error(e);
				import_jekyll_app.error_files.push(file);
				return 0;
			}
		}
	},
	created: function(){
		// 检查浏览器是否支持拖放上传。
		if('draggable' in global.document.createElement('span')){
			var holder = global.document.getElementById('jekyll_md_holder');
			holder.ondragover = function () { this.className = 'hover'; return false; };
			holder.ondragend = function () { this.className = ''; return false; };
			holder.ondrop = function (event) {
				event.preventDefault();
				this.className = '';
				import_jekyll_app.files = [];
				var files = event.dataTransfer.files;
				var results = [];
				for (var i = files.length - 1; i >= 0; i--) {
					var reader = new FileReader();
					reader.readAsText(files[i], 'UTF-8');
					// fuck javascript
					reader.onload = (function(file) {
						return function(event){
							var re = this.analysis_post(event.target.result, file);
							if(re && re['content']){
								import_jekyll_app.files.push({
									'url': file.name,
									'title': re['title'],
									'tags': re['tags'],
									'last_modified_time': file.lastModifiedDate,
									'name': file.name,
									'size': file.size,
									'content': re['content'],
									'check': true,
								});
							}
						}
					})(files[i]);
				}
			};
		} else {
			alert('Your Browser doesn\'t support drag files.');
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