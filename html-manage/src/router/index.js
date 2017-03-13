import Vue from 'vue'
import Router from 'vue-router'
import Blogs from '@/components/Blogs'
import BlogHomePanal from '@/components/Blogs/HomePanal'
import BlogSetting from '@/components/Blogs/HomePanal/Setting'
import BlogImportJekyll from '@/components/Blogs/HomePanal/Import_Jekyll'
import UserMe from '@/components/Users/UserMe'
import PostsPanel from '@/components/Blogs/PostsPanel'
import PostEditor from '@/components/Blogs/PostsPanel/PostEditor'

Vue.use(Router)

export default new Router({
	routes: [
		{
			path: '/blog/:blog/', component: Blogs,
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
					path: 'post/', component: PostsPanel, name: 'post-list', meta: {status: 'p'},
					children: [
						{
							path: ':post/', component: PostEditor, name: 'post-detail', meta: {status: 'p'},
						},
					],
				},
				{
					path: 'draft/', component: PostsPanel, name: 'draft-list', meta: {status: 'd'},
					children: [
						{
							path: ':post/', component: PostEditor, name: 'draft-detail', meta: {status: 'd'},
						},
					],
				},
				{
					path: 'trash/', component: PostsPanel, name: 'trash-list', meta: {status: 't'},
					children: [
						{
							path: ':post/', component: PostEditor,  name: 'trash-detail', meta: {status: 't'},
						},
					],
				},
			]
		},
		{
			path: '/me', component: UserMe, name: 'userme',
		},
		{
			path: '/', component: Blogs, name: 'index',
		},
	]
})
