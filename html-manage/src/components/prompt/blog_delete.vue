<template>
<div>
	<el-dialog v-model="display"
		@close="$emit('close', 'cancel');"
		:close-on-click-modal='true'
		:close-on-press-escape='false' size="tiny"
		title='删除博客'
		>
		<span>确认删除吗？这将删除与博客关联的所有博文、评论。</span>
		<span slot="footer" class="dialog-footer">
			<el-button type="danger" @click="$emit('close', 'delete')">删 除</el-button>
			<el-button @click="$emit('close', 'cancel');">取 消</el-button>
		</span>
	</el-dialog>
</div>
</template>

<script>
export default {
	data () {
		return {
			display: true,
		}
	},
};
</script>