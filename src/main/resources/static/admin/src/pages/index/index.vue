<template>
  <!-- 运营-首页 -->
  <div>
    <!--头部-->
    <base-info ref="baseInfo" />
    <!--小方块-->
    <grid-menu />
    <!--订单统计-->
    <visit-chart ref="visitChart" />
    <!--用户-->
    <user-chart ref="userChart" />
    <!-- <div class="open-image" v-if="openImage">
      <img src="@/assets/images/wechat_demo.png" alt="" />
      <span class="iconfont iconcha" @click="clear"></span>
    </div> -->
  </div>
</template>

<script>
import baseInfo from "./components/baseInfo";
import gridMenu from "./components/gridMenu";
import visitChart from "./components/visitChart";
import userChart from "./components/userChart";
import hotSearch from "./hot-search";
import userPreference from "./user-preference";
import { checkAuth } from "@/api/index";
import { auth } from "@/api/system";
import { Notice } from "iview";
import util from "@/libs/util";

export default {
  name: "index",
  components: {
    baseInfo,
    gridMenu,
    visitChart,
    userChart,
    hotSearch,
    userPreference,
  },
  data() {
    return {
      visitType: "day", // day, month, year
      visitDate: [new Date(), new Date()],
      openImage: false,
    };
  },
  mounted() {
    if (!util.cookies.get("auth")) {
      checkAuth()
        .then((res) => {})
        .catch((res) => {});
    }
    this.getAuth();
  },
  methods: {
    getAuth() {
      auth()
        .then((res) => {
          let data = res.data || {};
          if (data.auth_code && data.auth) {
            this.authCode = data.auth_code;
            this.auth = true;
          }
          this.openImage = true;
        })
        .catch((res) => {});
    },
    clear() {
      this.openImage = false;
    },
  },
};
</script>

<style lang="less">
.dashboard-console-visit {
  .ivu-radio-group-button .ivu-radio-wrapper {
    border: none !important;
    box-shadow: none !important;
    padding: 0 12px;
  }

  .ivu-radio-group-button .ivu-radio-wrapper:before,
  .ivu-radio-group-button .ivu-radio-wrapper:after {
    display: none;
  }
}

.open-image {
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  width: 130px;
  height: 580px;
  top: 50%;
  right: 40px;
  transform: translateY(-50%);
  z-index: 1000;
  cursor: pointer;

  img {
    width: 130px;
  }

  .iconfont {
    position: absolute;
    top: -20px;
    right: -20px;
    font-size: 20px;
    color: #ddd;
  }
}
</style>
