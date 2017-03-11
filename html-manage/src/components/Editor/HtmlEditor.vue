<template>
	<div style="height: 100%; overflow: hidden;">
		<div id="note-post-editor-html-container">
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
				$("#note-post-editor-html-container").html(this.model.rendered_html);
			}
		}
	},
	mounted: function(){
		var self = this;
		EDIT_HTML('note-post-editor-html-container', function(editor){
			self.model.rendered_html = editor.$txt.html();
			self.editor = editor;
		});
		this.reload();
	}
};

var EDIT_HTML = function(id, change) {
	log('EDIT_HTML: init html editor')
	var edit = function() {
		var html_editor = new wangEditor(id);
		html_editor.config.jsFilter = false;
		html_editor.config.uploadImgUrl = '/api/img/';
		html_editor.config.uploadHeaders = {
			'X-CSRFToken': getCookie('csrftoken'),
		};
		html_editor.config.uploadImgFileName = 'file'
		html_editor.onchange = function(){
			change(html_editor);
		}
		html_editor.create();
		return html_editor;
	}
	if(typeof(wangEditor)=='undefined') {
		var get_css = function(css) {
			$('head').append('<link rel="stylesheet" href="' + css + '" type="text/css" />');
		}
		get_css('//cdn.bootcss.com/wangeditor/2.1.20/css/wangEditor.min.css');
		$.getScript('//cdn.bootcss.com/wangeditor/2.1.20/js/wangEditor.min.js', function(){
			edit();
		});
	} else {
		edit();
	}
}
</script>

<style>
.wangEditor-container {
	height: 100%;
}
.wangEditor-txt {
	height: 100%;
}
</style>