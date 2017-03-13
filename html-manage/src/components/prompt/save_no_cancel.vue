<template>
<div>
	<el-dialog v-model="display"
		@close="$emit('close', 'cancel');"
		:close-on-click-modal='true'
		:close-on-press-escape='false' size="tiny">
		<span>内容未保存</span>
		<span slot="footer" class="dialog-footer">
			<el-button type="success" @click="$emit('close', 'save')">保 存</el-button>
			<el-button type="danger" @click="$emit('close', 'no')">不保存</el-button>
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