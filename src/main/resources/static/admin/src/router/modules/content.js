// +----------------------------------------------------------------------
// | CRMEB [ CRMEB赋能开发者，助力企业发展 ]
// +----------------------------------------------------------------------
// | Copyright (c) 2016~2021 https://www.crmeb.com All rights reserved.
// +----------------------------------------------------------------------
// | Licensed CRMEB并不是自由软件，未经许可不能去掉CRMEB相关版权
// +----------------------------------------------------------------------
// | Author: CRMEB Team <admin@crmeb.com>
// +----------------------------------------------------------------------
import BasicLayout from "@/layouts/basic-layout";

const pre = "content_";

export default {
  path: "/admin/content",
  name: "content",
  header: "content",
  meta: {
    // 授权标识
    auth: ["admin-content"],
  },
  component: BasicLayout,
  children: [
    {
      path: "community/topic",
      name: `${pre}topic`,
      meta: {
        auth: ["admin-community-topic"],
        title: "社区话题",
      },
      component: () => import("@/pages/content/community/topic"),
    },
    {
      path: "community/content",
      name: `${pre}content`,
      meta: {
        auth: ["admin-community-content"],
        title: "社区内容",
      },
      component: () => import("@/pages/content/community/content"),
    },
    {
      path: "community/addContent/:id?",
      name: `${pre}addContent`,
      meta: {
        auth: ["admin-community-addcontent"],
        title: "添加内容",
      },
      component: () => import("@/pages/content/community/addContent"),
    },
    {
      path: "community/comment",
      name: `${pre}comment`,
      meta: {
        auth: ["admin-community-comment"],
        title: "社区评论",
      },
      component: () => import("@/pages/content/community/comment"),
    },
    {
      path: "community/setting",
      name: `${pre}setting`,
      meta: {
        auth: ["admin-community-setting"],
        title: "社区设置",
      },
      component: () => import("@/pages/content/community/setting"),
    },
    {
      path: "article/index/:id?",
      name: `${pre}article`,
      meta: {
        auth: ["cms-article-index"],
        title: "文章管理",
      },
      component: () => import("@/pages/content/cms/article/index"),
    },
    {
      path: "article_category/index",
      name: `${pre}articleCategory`,
      meta: {
        auth: ["cms-article-category"],
        title: "文章分类",
      },
      component: () => import("@/pages/content/cms/articleCategory/index"),
    },
    {
      path: "article/add_article/:id?",
      name: `${pre}addArticle`,
      meta: {
        auth: ["cms-article-creat"],
        title: "文章添加",
      },
      component: () => import("@/pages/content/cms/addArticle/index"),
    },
    {
      path: 'live/live_room',
      name: `${pre}live_room`,
      meta: {
          auth: true,
          title: '直播间管理'
      },
      component: () => import('@/pages/content/live/index')
  },
  {
      path: 'live/add_live_room',
      name: `${pre}add_live_room`,
      meta: {
          auth: true,
          title: '直播间管理'
      },
      component: () => import('@/pages/content/live/creat_live')
  },
  {
      path: 'live/live_goods',
      name: `${pre}live_goods`,
      meta: {
          auth: true,
          title: '直播间商品管理'
      },
      component: () => import('@/pages/content/live/live_goods')
  },
  {
      path: 'live/add_live_goods',
      name: `${pre}add_live_goods`,
      meta: {
          auth: true,
          title: '直播间商品管理'
      },
      component: () => import('@/pages/content/live/add_goods')
  },
  {
      path: 'live/anchor',
      name: `${pre}anchor`,
      meta: {
          auth: true,
          title: '主播管理'
      },
      component: () => import('@/pages/content/live/anchor')
  },
  ],
};
