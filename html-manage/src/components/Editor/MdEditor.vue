<template>
<div class="container box-col" :class='{full_screen: is_full_screen}'>
	<div id="bar">
		<div>
			<el-tooltip effect="light" content="Ctrl + S" placement="top">
				<span @click='save'><i class="fa fa-floppy-o" aria-hidden="true"></i> Save</span>
			</el-tooltip>
		</div>
		<div class="center">
			<span @click='show("editor")' :class="{bolder: show_editor&&!show_html}">Markdown</span>
			<span @click='show("split")' :class="{bolder: show_editor&&show_html}">Split</span>
			<span @click='show("html")' :class="{bolder: !show_editor&&show_html}">Rendered</span>
		</div>
		<div>
			<el-tooltip effect="light" content="Alt + Enter" placement="top">
				<span @click='full_screen'><i class="fa fa-arrows-alt" aria-hidden="true"></i> FullScreen</span>
			</el-tooltip>
		</div>
	</div>
	<div class="content stretch">
		<textarea v-if='show_editor' id="editor-md-textarea" 
			class='markdown'
			@keydown.tab.prevent="insert_tab"
			@keydown.ctrl.S.prevent="save"
			@keydown.alt.enter.prevent='full_screen'
			v-model='model.content'>
		</textarea>
		<div class="seprate" v-if='show_editor&&show_html'></div>
		<div v-if='show_html'
			class="rendered" 
			v-html='model.rendered_html'></div>
	</div>
</div>
</template>


<script>
var RENDER_MARKDOWN = function(md){
	return marked(md).trim();
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
			log('MdEditor: model.content changed')
			log(this.model.content);
			log(this.model.rendered_html);
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
		},
		save: function(){
			this.$emit('save');
		},
	},
};
</script>

<style scoped>
.container {
	overflow: hidden;
}
.full_screen {
	position: absolute;
	left: 0;
	right: 0;
	top: 0;
	bottom: 0;
	padding: 7px;
	height: 98%;
	background-color: white;
	font-size: 1.2em;
	z-index: 1000;
}
#bar {
	width: 100%;
	display: flex;
	align-items: center;
	justify-content: space-between;
}
#bar span {
	cursor: pointer;
}
#bar .center {
	/*align-self: center;*/
	max-width: 50%;
}
.content {
	padding-top: 1em;
	display: flex;
	display: -webkit-flex;
	flex-shrink: 1;
	flex-grow: 1;
}
.markdown, .rendered {
	flex: 1;
	resize: none;
	overflow-y: scroll;
	word-break: break-all;
	padding: 0.8em;
	margin: 0;
}
.seprate {
	flex-basis: 0.1em;
}
.markdown {
	font-size: 1.1em;
	line-height: 1.5em;
}
.markdown,
.markdown:active,
.markdown:focus,
.markdown:hover,
.markdown:visited
 {
 	outline: none !important;
	border: 1px solid rgba(135, 135, 135, 0.62);
}
.rendered {
	border: 1px solid rgba(135, 135, 135, 0.62);
	padding-top: 0;
	padding-bottom: 0;
}
</style>