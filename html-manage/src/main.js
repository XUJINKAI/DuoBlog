// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import BUS from './API/BUS'

import iView from 'iview';
import 'iview/dist/styles/iview.css';
Vue.use(iView);

Vue.config.productionTip = false
window.DEBUG = (process.env.NODE_ENV !== 'production');

/* eslint-disable no-new */
var app = new Vue({
	el: '#app',
	router,
	template: '<div><App/></div>',
	components: { App },
	methods: {
		check_route: function(){
			if(this.$route.name=='index') {
				//TODO 得BUS先加载完blog_list再执行
				this.$router.push({ name: 'post-list', params: { blog: this.BUS.blog_list[0].pk}})
			}
		}
	},
	watch: {
		'$route': function(){
			this.check_route();
		}
	},
	mounted: function(){
		var self = this;
		self.BUS.$on('blog_changed', function(pk){
			if(pk) {
				self.$router.push({name: 'blog', params: {blog: pk}});
			} else {
				self.check_route();
			}
		})
	}
})

router.beforeEach((to, from, next) => {
	if(app.BUS.content_changed) {
		alert('not saved');
		next(false);
	} else {
		next();
	}
})

if(DEBUG) {
	window.BUS = BUS;
	window.app = app;
}