<template>
	<div id="note-post-editor" v-if='model'>
		<HtmlEditor v-if='model.content_type == "h"' :model='model'></HtmlEditor>
		<MdEditor v-else-if='model.content_type == "m"' :model='model'></MdEditor>
		<p v-else>Error Type.</p>
	</div>
</template>


<script>
import HtmlEditor from './HtmlEditor'
import MdEditor from './MdEditor'
export default {
	components: {
		HtmlEditor,
		MdEditor,
	},
	data: function(){
		return {
		};
	},
	watch: {
		'model.content': function(){
			this.content_changed();
		}
	},
	props: {
		model: Object,
	},
	methods: {
		content_changed: function(){
			this.$emit('editor_content_changed');
		}
	}
};
</script>