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

const pre = "agent_";
const meta = {
  auth: true,
};
export default {
  path: "/admin/agent",
  name: "agent",
  header: "agent",
  // redirect: {
  //     name: `${pre}agentManage`
  // },
  meta,
  component: BasicLayout,
  children: [
    {
      path: "agent_manage/index",
      name: `${pre}agentManage`,
      meta: {
        auth: ["agent-agent-manage"],
        title: "分销员管理",
      },
      component: () => import("@/pages/agent/agentManage"),
    },
    {
      path: "agreement",
      name: `${pre}agreementt`,
      meta: {
        auth: ["agent-agreement"],
        title: "分销说明",
      },
      component: () => import("@/pages/agent/agreement"),
    },
    {
      path: "division_list",
      name: `${pre}division`,
      meta: {
        auth: ["agent-division-index"],
        title: "区域代理列表",
      },
      component: () => import("@/pages/division/list/index"),
    },
    {
      path: "order",
      name: `${pre}order`,
      meta: {
        auth: ["agent-division-order"],
        title: "事业部订单",
      },
      component: () => import("@/pages/division/agent/order"),
    },
    {
      path: "agent_list",
      name: `${pre}agent`,
      meta: {
        auth: ["agent-division-agent-index"],
        title: "代理商列表",
      },
      component: () => import("@/pages/division/agent/index"),
    },
    {
      path: "statistics",
      name: `${pre}agent`,
      meta: {
        auth: ["agent-division-statistics"],
        title: "事业部统计",
      },
      component: () => import("@/pages/division/agent/statistics"),
    },
    
    {
      path: "apply_list",
      name: `${pre}agent`,
      meta: {
        auth: ["agent-division-agent-applyList"],
        title: "代理商申请",
      },
      component: () => import("@/pages/division/agent/applyList"),
    },
    {
      path: "promoter/apply",
      name: `${pre}agent`,
      meta: {
        auth: ["admin-agent-promoter-apply"],
        title: "分销员申请",
      },
      component: () => import("@/pages/division/promoter/apply"),
    },
  ],
};
