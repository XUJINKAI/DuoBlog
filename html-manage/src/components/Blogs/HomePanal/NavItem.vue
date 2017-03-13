<template>
	<li>
		<div
			:class=""
			v-if='model && !isRoot'
			v-bind:title='model.url'
		>
			<span @click="Toggle">{{ model.name }}</span>&nbsp;&nbsp;&nbsp;&nbsp;
			<span @click="deleteItem" v-if='!isRoot'>[-]</span>
			<span @click="addChild" v-if='!isRoot'>[+]</span>
			<span @click="MoveUp" v-if='!isRoot'>[↑]</span>
			<span @click="MoveDown" v-if='!isRoot'>[↓]</span>
		</div>
		<form v-if='edit'>
			<input type="" name="" v-model='model.name' placeholder="Title">
			<input type="" name="" v-model='model.url' v-if="!hasSubItems" placeholder="URL">
		</form>
		<ul v-if="hasSubItems || isRoot">
			<NavItem
				class="item"
				v-for="model in model.sub"
				:key='model.name'
				:model="model">
			</NavItem>
			<li class="add" @click="addChild">+</li>
		</ul>
	</li>
</template>

<script>
export default {
	name: 'NavItem',
	props: {
		model: Object
	},
	data: function () {
		return {
			edit: false,
		}
	},
	computed: {
		isFolder: function () {
			return this.model.sub;
		},
		hasSubItems: function () {
			return this.model && this.model.sub && this.model.sub.length;
		},
		isRoot: function() {
			return this.$parent.$parent==undefined;
		}
	},
	methods: {
		Toggle: function() {
			this.edit = !this.edit;
		},
		addChild: function() {
			if (!this.isFolder) {
				Vue.set(this.model, 'sub', []);
			}
			this.model.sub.push({
				name: 'new nav',
				url: '/posts/?tags=',
				sub: [],
			})
		},
		deleteItem: function(){
			this.$parent.model.sub.remove(this.model);
		},
		MoveUp:function() {
			var idx = $.inArray(this.model, this.$parent.model.sub);
			this.$parent.model.sub.move(idx, idx - 1);
		},
		MoveDown:function() {
			var idx = $.inArray(this.model, this.$parent.model.sub);
			this.$parent.model.sub.move(idx, idx + 1);
		},
	}
}
</script>
