// +----------------------------------------------------------------------
// | CRMEB [ CRMEB赋能开发者，助力企业发展 ]
// +----------------------------------------------------------------------
// | Copyright (c) 2016~2021 https://www.crmeb.com All rights reserved.
// +----------------------------------------------------------------------
// | Licensed CRMEB并不是自由软件，未经许可不能去掉CRMEB相关版权
// +----------------------------------------------------------------------
// | Author: CRMEB Team <admin@crmeb.com>
// +----------------------------------------------------------------------
import BasicLayout from '@/layouts/basic-layout';

const pre = 'community_';

export default {
    path: '/admin/community',
    name: 'community',
    header: 'community',
	meta: {
	    // 授权标识
	    auth: ['admin-community']
	},
    component: BasicLayout,
    children: [
        {
            path: 'topic',
            name: `${pre}topic`,
            meta: {
                auth: ['admin-community-topic'],
                title: '社区话题'
            },
            component: () => import('@/pages/community/topic')
        },
		{
		    path: 'content',
		    name: `${pre}content`,
		    meta: {
		        auth: ['admin-community-content'],
		        title: '社区内容'
		    },
		    component: () => import('@/pages/community/content')
		},
        {
            path: 'addContent/:id?',
            name: `${pre}addContent`,
            meta: {
                auth: ['admin-community-addcontent'],
                title: '添加内容'
            },
            component: () => import('@/pages/community/addContent')
        },
		{
		    path: 'comment',
		    name: `${pre}comment`,
		    meta: {
		        auth: ['admin-community-comment'],
		        title: '社区评论'
		    },
		    component: () => import('@/pages/community/comment')
		},
		{
		    path: 'setting',
		    name: `${pre}setting`,
		    meta: {
		        auth: ['admin-community-setting'],
		        title: '社区设置'
		    },
		    component: () => import('@/pages/community/setting')
		},
    ]
};