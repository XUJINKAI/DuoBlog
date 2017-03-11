import Vue from 'vue'
import Router from 'vue-router'
import Blogs from '@/components/Blogs'
// import Setting from '@/components/Setting'
// import BlogSetting from '@/components/Blog/Setting'
// import BlogPostsList from '@/components/Blog/PostsList'
// import BlogComment from '@/components/Blog/Comment'
// import BlogNavs from '@/components/Blog/Navs'

Vue.use(Router)

export default new Router({
	routes: [
		{
			path: '/',
			component: Blogs
		},
		// {
		// 	path: '/blog/:pk/',
		// 	component: Blogs,
		// 	children: [
		// 		{
		// 			path: '', component: BlogPostsList
		// 		},
		// 		{
		// 			path: 'setting', component: BlogSetting
		// 		},
		// 		{
		// 			path: 'posts', component: BlogPostsList
		// 		},
		// 		{
		// 			path: 'posts/:pk/', component: BlogPostsList
		// 		},
		// 		{
		// 			path: 'draft', component: BlogPostsList
		// 		},
		// 		{
		// 			path: 'trash', component: BlogPostsList
		// 		},
		// 		{
		// 			path: 'comment', component: BlogComment
		// 		},
		// 		{
		// 			path: 'navs', component: BlogNavs
		// 		},
		// 	]
		// },
		// {
		// 	path: '/setting',
		// 	component: Setting
		// }
	]
})
