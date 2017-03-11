<template>
	<div class="box-col" style="flex: 1; overflow: overlay; height: 100%;" :class='{full_screen: is_full_screen}'>
		<div style="">
			<span v-on:click='show("editor")' :class="{bolder: show_editor&&!show_html}">Markdown</span>
			<span v-on:click='show("split")' :class="{bolder: show_editor&&show_html}">Split</span>
			<span v-on:click='show("html")' :class="{bolder: !show_editor&&show_html}">Rendered</span>
			<span v-on:click='full_screen' style="float: right;"><i class="fa fa-arrows-alt" aria-hidden="true"></i></span>
		</div>
		<div class="stretch box" style="padding-top: 1em;">
			<textarea v-if='show_editor' id="editor-md-textarea" 
				class='stretch y-scroll'
				style="
				flex: 1;
				resize: none;
				overflow-y: scroll;
				" 
				v-on:keydown.tab.prevent="insert_tab"
				v-model='model.content'>
			</textarea>
			<div style="flex-basis: 2em;" v-if='show_editor&&show_html'></div>
			<div v-if='show_html'
				style="
				flex: 1;
				overflow-wrap: break-word;
    			overflow-y: scroll;
				" 
				v-html='model.rendered_html'></div>
		</div>
	</div>
</template>


<script>
$.getScript('http://cdn.bootcss.com/marked/0.3.6/marked.min.js');
var RENDER_MARKDOWN = function(md){
	var render = function() {
		return marked(md);
	}
	if(typeof(marked)=='undefined') {
		log('//MAKE RENDER MARKDOWN ASYNC.')
	}
	return render();
}

export default { 
	data: function(){
		return {
			show_editor: true,
			show_html: true,
			is_full_screen: false,
		};
	},
	props: {
		model: Object,
	},
	watch: {
		'model.content': function(){
			this.model.rendered_html = this.render(this.model.content);
		}
	},
	methods: {
		render: function(md){
			return RENDER_MARKDOWN(md);
		},
		insert_tab: function(){
			var el = document.getElementById('editor-md-textarea');
			var val = el.value,
                start = el.selectionStart,
                end = el.selectionEnd;

            // set textarea value to: text before caret + tab + text after caret
            el.value = val.substring(0, start) + '\t' + val.substring(end);

            // put caret at right position again
            el.selectionStart = el.selectionEnd = start + 1;
		},
		show: function(type) {
			if(type=='editor') {
				this.show_editor = true;
				this.show_html = false;
			} else if (type=='split') {
				this.show_editor = true;
				this.show_html = true;
			} else {
				this.show_editor = false;
				this.show_html = true;
			}
		},
		full_screen: function(){
			this.is_full_screen = !this.is_full_screen;
		}
	},
};
</script>

<style scoped>
.full_screen {
	position: absolute;
	left: 0;
	right: 0;
	top: 0;
	bottom: 0;
	padding: 20px;
	background-color: white;
}
</style>