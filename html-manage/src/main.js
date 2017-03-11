// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import BUS from './API/BUS'

Vue.config.productionTip = false
window.DEBUG = true;

/* eslint-disable no-new */
window.app = new Vue({
  el: '#app',
  router,
  template: '<div><App/></div>',
  components: { App }
})

if(DEBUG) {
	window.BUS = BUS;
}