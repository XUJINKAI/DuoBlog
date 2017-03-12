<template>
	<div id="wrapper">
		<div id="editor-html-container">
		</div>
	</div>
</template>

<script>
export default {
	data: function(){
		return {
			editor: null,
		};
	},
	props: {
		model: Object,
	},
	watch: {
		model: function(){
			this.reload();
		}
	},
	methods: {
		reload: function(){
			if(this.editor) {
				this.editor.$txt.html(this.model.rendered_html);
			} else {
				$("#editor-html-container").html(this.model.rendered_html);
			}
		}
	},
	created: function(){
	},
	mounted: function(){
		this.reload();
		var self = this;
		API.EDIT_HTML('editor-html-container', function(editor){
			self.model.rendered_html = editor.$txt.html();
			self.editor = editor;
		});
	}
};
</script>

<style scoped>
#wrapper {
	height: 100%;
	overflow: hidden;
}
#editor-html-container {
	height: 100%;
}
</style>
<style>
.wangEditor-container,
.editor-html-container {
	height: 100%;
}
</style>