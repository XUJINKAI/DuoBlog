<template>
<div class="filter-tags-container">
	<span style="font-weight: bolder;">Tags: </span>
	<span v-on:click='clear_tags' class='clear_tags'>Clear</span>
	<ul>
		<li v-for='tag in tags'>
			<input type="checkbox" :id="tag.name" :value='tag' v-model='selected_tags'>
			<span :for='tag.name' v-on:click='select_tag(tag);'>{{ tag.name }} {{ tag.count }}</span>
		</li>
	</ul>
</div>
</template>

<script>
export default {
	data: function(){
		return {
			selected_tags: [],
		}
	},
	props: {
		tags: Array,
	},
	methods: {
		clear_tags: function(){
			this.selected_tags = [];
		},
		select_tag: function(tag){
			this.clear_tags();
			this.selected_tags = [tag];
		},
	}
};
</script>

<style scoped>
.filter-tags-container ul {
	list-style: none;
	padding: 0;
	margin: 0;
}
.filter-tags-container ul li {
	margin-left: 5px;
}
.filter-tags-container .clear_tags {
	margin-left: 10px; 
	text-decoration: 
	underline; 
	color: gray;
}
.filter-tags-container ul li,
.filter-tags-container .clear_tags:hover {
	cursor: pointer;
}
</style>