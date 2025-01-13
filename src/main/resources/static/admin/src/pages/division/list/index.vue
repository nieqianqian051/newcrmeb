<template>
  <div>
    <Card :bordered="false" dis-hover class="ivu-mt" :padding="20">
      <Form
        ref="formValidate"
        :model="formValidate"
        :label-width="labelWidth"
        :label-position="labelPosition"
        @submit.native.prevent
        inline
      >
        <FormItem label="搜索：">
          <Input
            clearable
            placeholder="请输入姓名、UID"
            v-model="formValidate.keyword"
            class="input-add mr14"
          />
          <Button type="primary" @click="userSearchs">查询</Button>
        </FormItem>
      </Form>
    </Card>
    <Card :bordered="false" class="ivu-mt mt16">
      <Row class="ivu-mt box-wrapper">
        <Col :xs="24" :sm="24" ref="rightBox">
          <div class="mb20">
            <Button type="primary" @click="groupAdd('0')">添加区域代理</Button>
            <el-tooltip placement="right-start">
              <i class="el-icon-question ml10"></i>
              <div slot="content">
                <div>
                  团队层级说明：区域代理-代理商-员工。区域代理相当于总代理，设置成为区域代理之后，关联的用户会清除上级推广人
                </div>
                <div>
                  添加时候的管理员身份需要在，设置-管理权限-角色管理中设置对应的角色，区域代理可以使用添加时设置的管理员账号密码登录后台
                </div>
              </div>
            </el-tooltip>
          </div>

          <Table
            :data="userLists"
            :columns="columns"
            ref="table"
            class="mt25"
            highlight-row
            no-data-text="暂无数据"
            no-filtered-data-text="暂无筛选结果"
          >
            <template slot-scope="{ row }" slot="avatar">
              <div class="tabBox_img" v-viewer>
                <img v-lazy="row.avatar" />
              </div>
            </template>
            <template slot-scope="{ row }" slot="division_status">
              <i-switch
                v-model="row.division_status"
                :value="row.division_status"
                :true-value="1"
                :false-value="0"
                @on-change="onchangeIsShow(row)"
                size="large"
              >
                <span slot="open">开启</span>
                <span slot="close">关闭</span>
              </i-switch>
            </template>
            <template slot-scope="{ row, index }" slot="action">
              <a @click="jump(row.uid)">查看代理商</a>
              <Divider type="vertical"></Divider>
              <a @click="groupAdd(row.uid)">编辑</a>
              <Divider type="vertical"></Divider>
              <a @click="del(row, '删除员工', index)">删除</a>
            </template>
          </Table>
          <div class="acea-row row-right page">
            <Page
              :total="total"
              show-elevator
              show-total
              :page.sync="formValidate.page"
              @on-change="getList"
              :page-size="formValidate.limit"
            />
          </div>
        </Col>
      </Row>
    </Card>
    <Modal
      v-model="staffModal"
      title="代理商列表"
      class="order_box"
      :width="1000"
      footer-hide
    >
      <Table
        :data="clerkLists"
        :columns="columns2"
        ref="table"
        class="mt20"
        highlight-row
        no-data-text="暂无数据"
        no-filtered-data-text="暂无筛选结果"
      >
        <template slot-scope="{ row }" slot="avatar">
          <div class="tabBox_img" v-viewer>
            <img v-lazy="row.avatar" />
          </div>
        </template>
        <template slot-scope="{ row }" slot="division_percent">
          <span> {{ row.division_percent }}</span>
        </template>
        <template slot-scope="{ row }" slot="division_end_time">
          <span> {{ row.division_end_time | formatDate }}</span>
        </template>
      </Table>
      <div class="acea-row row-right page" v-if="staffModal">
        <Page
          :total="total2"
          show-elevator
          show-total
          :page.sync="clerkReqData.page"
          @on-change="getList"
          :page-size="clerkReqData.limit"
        />
      </div>
    </Modal>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { regionList, regionFrom, isShowApi, clerkList } from "@/api/agent";
import { formatDate } from "@/utils/validate";
export default {
  name: "agent_extra",
  data() {
    return {
      grid: {
        xl: 7,
        lg: 7,
        md: 12,
        sm: 24,
        xs: 24,
      },
      total: 0,
      total2: 0,
      userLists: [],
      columns: [
        {
          title: "用户UID",
          key: "uid",
          width: 80,
        },

        {
          title: "头像",
          slot: "avatar",
          width: 90,
        },
        {
          title: "名称",
          key: "division_name",
          width: 80,
        },
        {
          title: "邀请码",
          key: "division_invite",
          minWdith: 130,
        },
        {
          title: "分销比例",
          key: "division_percent",
          minWdith: 130,
        },
        {
          title: "代理商数量",
          key: "down_num",
          minWdith: 130,
        },
        {
          title: "截止时间",
          key: "division_end_time",
          minWdith: 130,
        },
        {
          title: "状态",
          slot: "division_status",
          minWdith: 130,
        },
        {
          title: "操作",
          slot: "action",
          width: 180,
        },
      ],
      columns2: [
        {
          title: "用户UID",
          key: "uid",
          width: 80,
        },

        {
          title: "头像",
          slot: "avatar",
          width: 90,
        },
        {
          title: "姓名",
          key: "nickname",
          width: 90,
        },
        {
          title: "分销比例",
          slot: "division_percent",
          minWidth: 80,
        },
        {
          title: "到期日期",
          key: "division_end_time",
          minWidth: 80,
        },
        {
          title: "员工数量",
          key: "down_num",
          minWidth: 80,
        },
      ],
      formInline: {
        uid: 0,
        proportion: 0,
        image: "",
      },
      FromData: null,
      loading: false,
      current: 0,
      formValidate: {
        page: 1,
        limit: 15,
        keyword: "",
      },
      staffModal: false,
      clerkReqData: {
        uid: 0,
        page: 1,
        limit: 15,
      },
      clerkLists: [],
    };
  },
  filters: {
    formatDate(time) {
      if (time !== 0) {
        let date = new Date(time * 1000);
        return formatDate(date, "yyyy-MM-dd");
      }
    },
  },
  computed: {
    ...mapState("media", ["isMobile"]),
    labelWidth() {
      return this.isMobile ? undefined : 80;
    },
    labelPosition() {
      return this.isMobile ? "top" : "right";
    },
  },
  mounted() {
    this.getList();
  },
  methods: {
    // 搜索
    userSearchs() {
      this.formValidate.page = 1;
      this.getList();
    },
    jump(uid) {
      this.clerkReqData.uid = uid;
      this.getClerkList();
    },
    getClerkList() {
      this.clerkReqData.division_type = 2;
      clerkList(this.clerkReqData).then((res) => {
        this.clerkLists = res.data.list;
        this.total2 = res.data.count;
        this.staffModal = true;
      });
    },
    // 列表
    getList() {
      this.loading = true;
      this.formValidate.division_type = 1;
      regionList(this.formValidate)
        .then(async (res) => {
          let data = res.data;
          this.userLists = data.list;
          this.total = data.count;
          this.loading = false;
        })
        .catch((res) => {
          this.loading = false;
          this.$Message.error(res.msg);
        });
    },
    // 添加表单
    groupAdd(id) {
      this.$modalForm(regionFrom(id))
        .then((res) => {
          this.getList();
        })
        .catch((err) => {});
    },
    // 修改是否显示
    onchangeIsShow(row) {
      let data = {
        id: row.uid,
        status: row.division_status,
      };
      isShowApi(data)
        .then(async (res) => {
          this.$Message.success(res.msg);
        })
        .catch((res) => {
          this.$Message.error(res.msg);
        });
    },
    // 编辑
    edit(row) {},
    // 删除
    del(row, tit, num) {
      let delfromData = {
        title: tit,
        method: "DELETE",
        uid: row.uid,
        url: `agent/division/del/${row.uid}`,
      };
      this.$modalSure(delfromData)
        .then((res) => {
          this.$Message.success(res.msg);
          this.userLists.splice(num, 1);
        })
        .catch((res) => {
          this.$Message.error(res.msg);
        });
    },
  },
};
</script>

<style scoped lang="stylus">
.ivu-form-item {
  margin-bottom: 0;
}

.picBox {
  display: inline-block;
  cursor: pointer;

  .upLoad {
    width: 58px;
    height: 58px;
    line-height: 58px;
    border: 1px dotted rgba(0, 0, 0, 0.1);
    border-radius: 4px;
    background: rgba(0, 0, 0, 0.02);
  }

  .pictrue {
    width: 60px;
    height: 60px;
    border: 1px dotted rgba(0, 0, 0, 0.1);
    margin-right: 10px;

    img {
      width: 100%;
      height: 100%;
    }
  }
}

::v-deep .ivu-menu-vertical .ivu-menu-item-group-title {
  display: none;
}

::v-deep .ivu-menu-vertical.ivu-menu-light:after {
  display: none;
}

.left-wrapper {
  height: 904px;
  background: #fff;
  border-right: 1px solid #f2f2f2;
}

.menu-item {
  z-index: 50;
  position: relative;
  display: flex;
  justify-content: space-between;
  word-break: break-all;
}

.icon-box {
  z-index: 3;
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  display: none;
}

&:hover .icon-box {
  display: block;
}

.right-menu {
  z-index: 10;
  position: absolute;
  right: -106px;
  top: -11px;
  width: auto;
  min-width: 121px;
}

.tabBox_img {
  width: 36px;

  height 36px {
    border-radius: 4px;
  }

  cursor pointer {
    img {
      width: 100%;
      height: 100%;
    }
  }
}
</style>
