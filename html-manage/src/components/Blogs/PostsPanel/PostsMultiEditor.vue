<template>
<div id="wrapper">
	<div id="operator">
		<button @click="$emit('delete_all')">Delete</button>
	</div>
	<table id="list">
		<thead>
			<tr>
				<th>Title</th>
				<th>Abstract</th>
				<th>Tags</th>
				<th>Comments</th>
				<th>Status</th>
				<th>Views</th>
				<th>Modified</th>
				<th>Create</th>
				<th>Modified</th>
			</tr>
		</thead>
		<tr v-for='post in posts'>
			<th>{{ post.title }}</th>
			<th>{{ post.abstract }}</th>
			<th></th> 
			<th>{{ post.comments }}</th>
			<th>{{ post.status | status_filter }}</th>
			<th>{{ post.views_count }}</th>
			<th>{{ post.modified_count }}</th>
			<th>{{ post.create_time | fromNow }}</th>
			<th>{{ post.last_modified_time | fromNow }}</th>
		</tr>
	</table>
</div>
</template>

<script>
export default {
	props: {
		posts: Array,
	},
	methods: {
	},
	filters: {
		fromNow: function(time) {
			return moment(time).fromNow();
		},
		status_filter: function(status){
			var map = {
				's': 'Sticky',
				'p': 'Public',
				'h': 'Hidden',
				'x': 'Private',
			}
			return map[status];
		},
	},
}
</script>

<style scoped>
#wrapper {

}
#operator {

}
#list {
	width: 100%;
	overflow-y: scroll;
}
</style>