<template>
<div>
	<el-dialog v-model="display"
		@close="display=true"
		:close-on-click-modal='false'
		:close-on-press-escape='false'
		:show-close='false'
		size="tiny"
		title='登录'
		>
		<span>用户名</span>
		<el-input type='input' v-model='username'></el-input>
		<span>密码</span>
		<el-input type='password' v-model='password'></el-input>
		<span slot="footer" class="dialog-footer">
			<el-button type="primary" @click="login">登 录</el-button>
		</span>
	</el-dialog>
</div>
</template>

<script>
export default {
	data () {
		return {
			display: true,
			username: '',
			password: '',
		}
	},
	methods: {
		login: function(){
			this.$emit('login', this.username, this.password);
		}
	}
};
</script>