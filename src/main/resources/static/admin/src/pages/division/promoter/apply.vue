<template>
  <div>
    <Card :bordered="false" dis-hover class="ivu-mt" :padding="0">
      <div class="new_card_pd">
        <Form
          ref="formValidate"
          :model="formValidate"
          :label-width="labelWidth"
          :label-position="labelPosition"
          @submit.native.prevent
          inline
        >
          <FormItem label="状态：">
            <Select
              clearable
              v-model="formValidate.status"
              placeholder="请选择状态"
              @on-change="userSearchs"
              class="input-add"
            >
              <Option
                :value="item.id"
                v-for="(item, index) in statusList"
                :key="index"
                :label="item.status_name"
              ></Option>
            </Select>
          </FormItem>
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
      </div>
    </Card>
    <Card :bordered="false" class="ivu-mt mt16">
      <Row class="ivu-mt box-wrapper">
        <Col :xs="24" :sm="24" ref="rightBox">
          <Table
            :data="userLists"
            :columns="columns"
            ref="table"
            highlight-row
            no-data-text="暂无数据"
            no-filtered-data-text="暂无筛选结果"
          >
            <template slot-scope="{ row }" slot="images">
              <div class="pictrue-box" v-if="row.images.length">
                <div
                  v-viewer
                  v-for="(item, index) in row.images || []"
                  :key="index"
                >
                  <img class="pictrue mr10" v-lazy="item" :src="item" />
                </div>
              </div>
            </template>
            <template slot-scope="{ row }" slot="status">
              <span v-if="row.status == 0">申请中</span>
              <span v-if="row.status == 1" class="colorgreen">已通过</span>
              <span v-if="row.status == 2" class="colorred">已拒绝</span>
            </template>
            <template slot-scope="{ row, index }" slot="action">
              <a v-if="row.status == 0" @click="groupAdd(row, 1)">同意</a>
              <Divider v-if="row.status == 0" type="vertical" />
              <a v-if="row.status == 0" @click="groupAdd(row, 2)">拒绝</a>
              <Divider type="vertical" v-if="row.status == 0" />
              <a @click="del(row, '删除申请', index)">删除</a>
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
  </div>
</template>

<script>
import { mapState } from "vuex";
import { promoterList, promoterFrom, isShowApi, clerkList } from "@/api/agent";
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
      formInline: {
        uid: 0,
        proportion: 0,
        image: "",
      },
      columns: [
        {
          title: "编号",
          key: "id",
          width: 80,
        },
        {
          title: "用户UID",
          key: "uid",
          width: 80,
        },
        {
          title: "用户昵称",
          key: "nickname",
          minWidth: 120,
        },
        {
          title: "分销员电话",
          key: "phone",
          minWidth: 120,
        },
        {
          title: "分销员姓名",
          key: "real_name",
          minWidth: 80,
        },
        {
          title: "手机号",
          key: "phone",
          minWidth: 80,
        },
        {
          title: "申请状态",
          slot: "status",
          minWidth: 140,
        },
        {
          title: "申请时间",
          key: "add_time",
          minWidth: 140,
        },
        {
          title: "操作",
          slot: "action",
          width: 160,
        },
      ],
      statusList: [
        {
          status_name: "申请中",
          id: 0,
        },
        {
          status_name: "已同意",
          id: 1,
        },
        {
          status_name: "已拒绝",
          id: 2,
        },
      ],
      FromData: null,
      loading: false,
      current: 0,
      formValidate: {
        page: 1,
        limit: 15,
        keyword: "",
        status: "all",
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
        return formatDate(date, "yyyy-MM-dd hh:mm");
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
    userSearchs() {
      this.formValidate.page = 1;
      this.getList();
    },
    jump(uid) {
      this.clerkReqData.uid = uid;
      this.getClerkList();
    },
    getClerkList() {
      this.clerkReqData.division_type = 3;
      clerkList(this.clerkReqData).then((res) => {
        this.clerkLists = res.data.list;
        this.total2 = res.data.count;
        this.staffModal = true;
      });
    },
    // 列表
    getList() {
      this.loading = true;
      promoterList(this.formValidate)
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
    pageChange(index) {
      this.formValidate.page = index;
      this.getList();
    },
    clerkPageChange() {
      this.clerkReqData.page = index;
      this.getClerkList();
    },
    // 审批申请
    groupAdd(row, type) {
      let delfromData = {
        title: type == 1 ? "同意申请" : "拒绝申请",
        method: "GET",
        uid: row.id,
        url: `agent/promoter/apply/examine/${row.id}/${row.uid}/${type}`,
      };
      this.$modalSure(delfromData)
        .then((res) => {
          this.$Message.success(res.msg);
          this.getList();
        })
        .catch((res) => {
          this.$Message.error(res.msg);
        });
    },
    // 删除
    del(row, tit, num) {
      let delfromData = {
        title: tit,
        method: "DELETE",
        uid: row.id,
        url: `agent/promoter/apply/del/${row.id}`,
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
/deep/ .ivu-form-item {
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

.pictrue-box {
  display: flex;
  align-item: center;
}

.pictrue {
  width: 25px;
  height: 25px;
}
.colorred {
  color: #ff5722;
}
.colorgreen {
  color: #009688;
}
</style>
