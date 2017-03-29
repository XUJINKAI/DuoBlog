import Vue from 'vue'
import Router from 'vue-router'
import BlogView from '@/components/Blogs/BlogView'
import BlogHomePanal from '@/components/Blogs/HomePanal'
import BlogSetting from '@/components/Blogs/HomePanal/Setting'
import BlogImportJekyll from '@/components/Blogs/HomePanal/Import_Jekyll'
import SettingView from '@/components/Setting/SettingView'
import About from '@/components/Setting/About'
import UserMe from '@/components/Users/UserMe'
import PostsPanel from '@/components/Blogs/PostsPanel'
import PostEditor from '@/components/Blogs/PostsPanel/PostEditor'
import TrashPanel from '@/components/Blogs/TrashPanel'

Vue.use(Router)

export default new Router({
	routes: [
		{
			path: '/blog/:blog/', component: BlogView,
			children: [
				{
					path: '', component: BlogHomePanal,
					children: [
						{
							path: '', component: BlogSetting, name: 'blog',
						},
						{
							path: 'import-jekyll', component: BlogImportJekyll, name: 'blog-import-jekyll',
						},
					]
				},
				{
					path: 'post/', component: PostsPanel, name: 'post-list',
					children: [
						{
							path: ':post/', component: PostEditor, name: 'post-detail',
						},
					],
				},
				{
					path: 'trash/', component: TrashPanel, name: 'trash',
				},
			]
		},
		{
			path: '/setting', component: SettingView,
			children: [
				{
					path: '', component: About, name: 'setting',
				}
			]
		},
		{
			path: '/me', component: UserMe, name: 'userme',
		},
		{
			path: '/', name: 'index',
		},
	]
})
