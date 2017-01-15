{% extends './base.html' %}

{% block title %}Blogs{% endblock %}


{% block css %}
<style>
#posts_app {
	margin-top: 10px;
}
.post_title:hover {
	cursor: default;
	text-decoration: none;
}
.post_title {
}
.post_item_selected {
	background: #95ff9f;
}
.post_item:hover {
	background: antiquewhite;
}
.tags_filter select {
	border:none;
	white-space: normal;
	width: 100%;
	height: auto;
	overflow: auto;
}
.tags_filter option {
	border:1px solid #000;
	background-color:white;
	margin-right: 5px;
	display:inline-block;
}
.full_screen_wrapper {
	top: 0px;
    left: 0px;
    right: 0px;
    bottom: 0px;
    position: absolute;
    z-index: 1000;
    background: white;
}
.full_screen_content {
	margin: 20px 0 0 20px;
	background: white;
}
</style>
{% endblock %}


{% block content %}
<div class="row">
	<div id="posts_app">
		<div v-bind:class="{full_screen_wrapper: is_fullscreen}">
			<div v-bind:class="{full_screen_content: is_fullscreen}">
				<a v-on:click="is_fullscreen=!is_fullscreen" class="pull-right"><i class="fa fa-arrows-alt" aria-hidden="true"></i></a>
				<div id="selector_div">
					<span>${ page }/${ page_max }</span>
					<button class="btn-default" v-on:click='goto_offset(offset-limit)'>Previous</button>
					<button class="btn-default" v-on:click='goto_offset(offset+limit)'>Next</button>
					<select v-on:change="limit_option_change();" id="limit_select">
						<option>20</option>
						<option>50</option>
						<option>100</option>
						<option>All</option>
					</select>
					<div class="tags_filter">
						<button v-for='tag in tags' v-on:click="toggle_check_filter($event, tag);">${ tag }</button>
					</div>
				</div>
				<div id="operation_div">
					<span>Select ${ check_count }/${ posts.length }</span>
					<button class="btn-danger" v-on:click="delete_select_posts();">Delete</button>
					<span>Tags:</span>
					<button class="btn-primary">Add</button>
					<button class="btn-info">Remove</button>
					<span>Blog</span>
					<span>Comments</span>
					<span>Sticky</span>
					<span>Status</span>
					<button class="btn-default">edit</button>
				</div>
				<div class="row">
					<div class="col-md-12">
						<table style="width:100%">
							<thead>
								<tr>
									<th><input type="checkbox" name="" v-bind:checked="is_all_check" v-on:click="check_all();"></th>
									<th style="max-width: 100px;">Title</th>
									<th>Tags</th>
									<th>Blog</th>
									<th>Comments</th>
									<th>Sticky</th>
									<th>Status</th>
									<th>Views</th>
									<th>Modified</th>
									<th>Create</th>
									<th>Modified</th>
								</tr>
							</thead>
							<tr v-for='post in posts' v-on:click="check_post($event, post, true);" v-bind:class='{post_item_selected: post.check, post_item: !post.check}'>
								<th><input type="checkbox" name="post.title" v-bind:checked="post.check" v-on:click="check_post($event, post);"></th>
								<th><a class="post_title" href="javascript:void(0);">${ post.title }</a></th>
								<th><span v-for='tag in post.tags'><a href="javascript:void(0);">${ tag }, </a></span></th> 
								<th>${ post.blog }</th>
								<th><input type="checkbox" v-bind:checked="post.comment" v-model="post.comment" v-on:click="$event.stopPropagation()"></th>
								<th><input type="checkbox" v-bind:checked="post.sticky" v-model="post.sticky" v-on:click="$event.stopPropagation()"></th>
								<th>${ post.status }</th>
								<th>${ post.views_count }</th>
								<th>${ post.modified_count }</th>
								<th>${ post.create_time | fromNow }</th>
								<th>${ post.last_modified_time | fromNow }</th>
							</tr>
						</table>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
{% endblock %}


{% block js %}
<script>
var posts_app = new Vue({
	delimiters: ['${', '}'],
	el: '#posts_app',
	data: {
		url: "{% url 'api:post-list' %}",
		limit: 20,
		offset: 0,
		total_count: null,
		posts: [],
		previous: '',
		next: '',
		tags: [],
		select_tags: [],
		tags_set: new Set(),
		last_checked_post: null,
		is_fullscreen: false,
	},
	computed: {
		query_str: function() {
			return '?limit=' + parseInt(this.limit).toString() + '&offset=' + parseInt(this.offset).toString();
		},
		page: function() {
			return Math.ceil(this.offset/this.limit) + 1;
		},
		page_max: function() {
			return Math.ceil(this.total_count/this.limit);
		},
		offset_max: function() {
			return Math.floor(this.total_count/this.limit) * this.limit;
		},
		check_count: function() {
			var count = 0;
			for (var i = 0; i < this.posts.length; i++) {
				if(this.posts[i].check) {
					count++;
				}
			}
			return count;
		},
		is_all_check: function() {
			return this.check_count == this.posts.length;
		},
		checked_slugs: function(){
			var slugs = [];
			for (var i = 0; i < this.posts.length; i++) {
				if(this.posts[i].check) {
					slugs.push(this.posts[i].slug)
				}
			}
			return slugs;
		},
	},
	methods: {
		fresh_data: function(){
			var self = this;
			$.ajax({
				url: this.url + this.query_str,
				method: 'GET',
				headers: {
					'X-CSRFToken': getCookie('csrftoken'),
				},
				dataType: 'json',
				data: {
				},
				success: function(data){
					window.history.pushState(null, null, window.location.pathname + self.query_str);
					self.previous = data.previous;
					self.next = data.next;
					self.total_count = data.count;
					self.posts = [];
					self.tags_set = new Set();
					for (var i = 0; i < data.results.length; i++) {
						self.add_post(data.results[i])
					}
					self.tags = [...self.tags_set]
				},
				error: function(data){
					console.log(data.responseText);
				}
			})
		},
		delete_select_posts: function(){
			var self = this;
			$.ajax({
				url: this.url,
				method: 'DELETE',
				headers: {
					'X-CSRFToken': getCookie('csrftoken'),
				},
				dataType: 'json',
				data: {
					'delete_slugs': JSON.stringify(self.checked_slugs),
				},
				success: function(data){
					self.fresh_data();
				},
				error: function(data){
					console.log(data.responseText);
					alert(data.responseText);
				}
			})
		},
		add_post: function(post) {
			post.check = false;
			for (var i = 0; i < post.tags.length; i++) {
				this.tags_set.add(post.tags[i]);
			}
			this.posts.push(post);
		},
		goto_offset: function(offset) {
			if (offset < 0) {
				offset = 0;
			}
			if (offset > this.offset_max) {
				offset = this.offset_max;
			}
			this.offset = offset;
			this.fresh_data();
		},
		check_all: function(all){
			var check = !this.is_all_check;
			if(all!==undefined) {
				check = all;
			}
			for (var i = 0; i < this.posts.length; i++) {
				this.posts[i].check = check;
			}
		},
		check_post: function(event, post, uncheck_others){
			if(uncheck_others===true) {
				this.check_all(false);
			}
			post.check = !post.check;
			if(post.check) {
				this.last_checked_post = post;
			} else {
				this.last_checked_post = null;
			}
		},
		preview_post: function(post) {
			window.open(post.html_url, "_blank");
		},
		limit_option_change: function(value) {
			this.limit = parseInt($("#limit_select").val());
			this.fresh_data();
		},
		show_post_menu: function(event, post) {
			//TODO
		},
		toggle_check_filter: function(event, text) {
		},
		filter_by_select_tags: function() {
			if (this.select_tags.length > 0) {
				this.check_all(true);
				for (var i = 0; i < this.posts.length; i++) {
					if (this.posts[i].tags.length > 0) {
						for (var j = 0; j < this.select_tags.length; j++) {
							if ( $.inArray(this.select_tags[j], this.posts[i].tags) < 0) {
								this.posts[i].check = false;
							}
						}
					} else {
						this.posts[i].check =false;
					}
				}
			} else {
				this.check_all(false);
			}
		},
	},
	filters: {
		fromNow: function(time) {
			return moment(time).fromNow();
		}
	}
})
function getParameterByName(name, url) {
	if (!url) {
	  url = window.location.href;
	}
	name = name.replace(/[\[\]]/g, "\\$&");
	var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
		results = regex.exec(url);
	if (!results) return null;
	if (!results[2]) return '';
	return decodeURIComponent(results[2].replace(/\+/g, " "));
}
$(function(){
	var limit = getParameterByName('limit');
	if(limit) {
		posts_app.limit = parseInt(limit);
	}
	var offset = getParameterByName('offset');
	if(offset) {
		posts_app.offset = parseInt(offset);
	}
	// get data
	posts_app.fresh_data();
	// bind contextmenu
	// if (document.addEventListener) { // IE >= 9; other browsers
	// 	document.addEventListener('contextmenu', function(e) {
	// 		e.preventDefault();
	// 	}, false);
	// } else { // IE < 9
	// 	document.attachEvent('oncontextmenu', function() {
	// 	window.event.returnValue = false;
	// 	});
	// }
})
</script>
{% endblock %}