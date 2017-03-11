import Vue from 'vue'

export default BUS;

var BUS = new Vue({
	template: '<div></div>',
	data: function(){
		var self = this;
		API.blog_list(function(data){
			self.blogs_list = data;
		})
		return {
			blogs_list: []
		}
	}
});
Vue.use(function(Vue){
	Vue.prototype.BUS = BUS;
	Vue.mixin({
		created: function(){
			this.BUS = BUS;
			this.$data.$BUS = BUS.$data;
		}
	})
});
