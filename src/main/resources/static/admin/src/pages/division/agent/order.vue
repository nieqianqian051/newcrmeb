<template>
  <!-- 订单-售后订单 -->
  <div>
    <Card :bordered="false" dis-hover class="ivu-mt" :padding="0">
      <div class="new_card_pd">
        <!-- 筛选条件 -->
        <Form
          ref="pagination"
          :model="pagination"
          :label-width="labelWidth"
          inline
          :label-position="labelPosition"
          @submit.native.prevent
        >
          <FormItem label="订单搜索：" prop="real_name" label-for="real_name">
            <Input
              v-model="pagination.real_name"
              placeholder="请输入"
              element-id="name"
              clearable
              class="input-add"
              maxlength="20"
            >
              <Select
                v-model="pagination.field_key"
                slot="prepend"
                style="width: 80px"
                default-label="全部"
              >
                <Option value="all">全部</Option>
                <Option value="order_id">订单号</Option>
                <Option value="uid">用户UID</Option>
                <Option value="real_name">用户姓名</Option>
                <Option value="user_phone">用户电话</Option>
                <Option value="title">商品名称</Option>
                <Option value="total_num">商品件数</Option>
              </Select>
            </Input>
          </FormItem>
          <FormItem label="创建时间：">
            <DatePicker
              @on-change="onchangeTime"
              :value="timeVal"
              format="yyyy/MM/dd"
              type="datetimerange"
              placement="bottom-start"
              placeholder="自定义时间"
              style="width: 250px; margin-right: 14px"
              class="mr20"
              :options="options"
            ></DatePicker>
          </FormItem>
          <FormItem label="团队选择：" v-if="showDivisionFilter == 0">
            <Select
              clearable
              v-model="pagination.division_id"
              placeholder="请选择团队"
              @on-change="agentSearch"
              class="input-add"
            >
              <Option
                v-for="(item, index) in divisionList"
                :key="index"
                v-bind="item"
              ></Option>
            </Select>
          </FormItem>
          <FormItem label="代理商：">
            <Select
              clearable
              v-model="pagination.division_agent_id"
              placeholder="请选择代理商"
              @on-change="search"
              class="input-add"
            >
              <Option
                v-for="(item, index) in divisionAgentList"
                :key="index"
                v-bind="item"
              ></Option>
            </Select>
            <Button type="primary" class="ml14" @click="search()">查询</Button>
          </FormItem>
        <!--  -->
        </Form>
      </div>
    </Card>
    <Card :bordered="false" dis-hover class="ivu-mt">
      <div>
        <Button @click="exports">导出</Button>
      </div>
      <vxe-table
        ref="xTable"
        :loading="loading"
        row-id="id"
        :expand-config="{ accordion: true }"
        :checkbox-config="{ reserve: true }"
        :data="orderList"
        class="mt-20"
      >
        <vxe-column type="expand" width="35">
          <template #content="{ row }">
            <div class="tdinfo">
              <Row class="expand-row">
                <Col span="8">
                  <span class="expand-key">商品总价：</span>
                  <span class="expand-value" v-text="row.total_price"></span>
                </Col>
                <Col span="8">
                  <span class="expand-key">下单时间：</span>
                  <span class="expand-value" v-text="row.add_time"></span>
                </Col>
                <Col span="8">
                  <span class="expand-key">推广人：</span>
                  <span
                    class="expand-value"
                    v-text="row.spread_nickname ? row.spread_nickname : '无'"
                  ></span>
                </Col>
              </Row>
              <Row class="expand-row">
                <Col span="8">
                  <span class="expand-key">用户备注：</span>
                  <span
                    class="expand-value"
                    v-text="row.mark ? row.mark : '无'"
                  ></span>
                </Col>
                <Col span="8">
                  <span class="expand-key">商家备注：</span>
                  <span
                    class="expand-value"
                    v-text="row.remark ? row.remark : '无'"
                  ></span>
                </Col>
              </Row>
            </div>
          </template>
        </vxe-column>
        <vxe-column field="order_id" title="订单号" min-width="175">
          <template v-slot="{ row }">
            <Tooltip
              :transfer="true"
              theme="dark"
              max-width="300"
              :delay="600"
              content="用户已删除"
              v-if="row.is_del === 1 && row.delete_time == null"
            >
              <span style="color: #ed4014; display: block">{{
                row.order_id
              }}</span>
            </Tooltip>
            <span
              @click="changeMenu(row, '2')"
              v-else
              style="color: #2d8cf0; display: block; cursor: pointer"
              >{{ row.order_id }}</span
            >
          </template>
        </vxe-column>
        <vxe-column
          field="pink_name"
          title="订单类型"
          min-width="120"
        ></vxe-column>
        <vxe-column field="nickname" title="用户信息" min-width="130">
          <template v-slot="{ row }">
            <a>{{ row.nickname }}</a>
            <span style="color: #ed4014" v-if="row.delete_time != null">
              (已注销)</span
            >
          </template>
        </vxe-column>
        <vxe-column field="info" title="商品信息" min-width="330">
          <template v-slot="{ row }">
            <Tooltip :transfer="true" theme="dark" max-width="300" :delay="600">
              <div class="tabBox" v-for="(val, i) in row._info" :key="i">
                <div class="tabBox_img" v-viewer>
                  <img
                    v-lazy="
                      val.cart_info.productInfo.attrInfo
                        ? val.cart_info.productInfo.attrInfo.image
                        : val.cart_info.productInfo.image
                    "
                  />
                </div>
                <span class="tabBox_tit line1">
                  <span class="font-color-red" v-if="val.cart_info.is_gift"
                    >赠品</span
                  >

                  {{ val.cart_info.productInfo.store_name + " | " }}
                  {{
                    val.cart_info.productInfo.attrInfo
                      ? val.cart_info.productInfo.attrInfo.suk
                      : ""
                  }}
                </span>
                <span>{{ " x " + val.cart_info.cart_num }}</span>
              </div>
              <div slot="content">
                <div v-for="(val, i) in row._info" :key="i">
                   <p class="font-color-red" v-if="val.cart_info.is_gift">赠品</p>
                <p>{{ val.cart_info.productInfo.store_name }}</p>
                <p> {{ val.cart_info.productInfo.attrInfo? val.cart_info.productInfo.attrInfo.suk: ''}}</p>
                <p class="tabBox_pice">{{'￥' + val.cart_info.sum_price +' x ' + val.cart_info.cart_num }} </p>
                </div>
              </div>
            </Tooltip>
          </template>
        </vxe-column>
        <vxe-column
          field="pay_price"
          title="实际支付"
          align="center"
          min-width="70"
        >
          <template v-slot="{ row }">
            <span>{{ row.paid > 0 ? row.pay_price : 0 }}</span>
          </template>
        </vxe-column>
        <vxe-column
          field="_pay_time"
          title="支付时间"
          min-width="150"
        ></vxe-column>
        <vxe-column field="pay_type_name" title="支付类型" min-width="100">
          <template v-slot="{ row }">
            <span>{{ row.pay_type_name }}</span>
          </template>
        </vxe-column>
        <vxe-column field="statusName" title="订单状态" min-width="100">
          <template v-slot="{ row }">
            <Tag color="default" size="medium" v-show="row.status == 3">{{
              row.status_name.status_name
            }}</Tag>
            <Tag color="orange" size="medium" v-show="row.status == 4">{{
              row.status_name.status_name
            }}</Tag>
            <Tag
              color="orange"
              size="medium"
              v-show="row.status == 1 || row.status == 2 || row.status == 5"
              >{{ row.status_name.status_name }}</Tag
            >
            <Tag color="red" size="medium" v-show="row.status == 0">{{
              row.status_name.status_name
            }}</Tag>
            <Tag
              color="orange"
              size="medium"
              v-if="!row.is_all_refund && row.refund.length"
              >部分退款中</Tag
            >
            <Tag
              color="orange"
              size="medium"
              v-if="
                row.is_all_refund && row.refund.length && row.refund_type != 6
              "
              >退款中</Tag
            >
            <div class="pictrue-box" size="medium" v-if="row.status_name.pics">
              <div
                v-viewer
                v-for="(item, index) in row.status_name.pics || []"
                :key="index"
              >
                <img class="pictrue mr10" v-lazy="item" :src="item" />
              </div>
            </div>
          </template>
        </vxe-column>
      </vxe-table>
      <div class="acea-row row-right page">
        <Page
          :total="total"
          :current="pagination.page"
          show-elevator
          show-total
          @on-change="pageChange"
          :page-size="pagination.limit"
        />
      </div>
    </Card>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { getDivisionOrder } from "@/api/order";
import { getDivisionOptionApi, getDivisionAgentOptionApi, getDivisionOrderExportApi } from "@/api/agent"
import timeOptions from "@/utils/timeOptions";
import exportExcel from "@/utils/newToExcel.js";
export default {
  data() {
    return {
      openErp: false,
      tbody: [],
      num: [],
      orderDatalist: null,
      loading: false,
      FromData: null,
      total: 0,
      orderId: 0,
      pagination: {
        page: 1,
        limit: 15,
        real_name: "",
        field_key: "",
        time: "",
        division_id:"",
        division_agent_id:""
      },
      options: timeOptions,
      timeVal: [],
      orderList: [],
      divisionList:[],
      divisionAgentList:[]
    };
  },
  computed: {
    ...mapState("order", ["orderChartType"]),
    // ...mapState("admin/layout", ["isMobile"]),
    labelWidth() {
      return this.isMobile ? undefined : 96;
    },
    labelPosition() {
      return this.isMobile ? "top" : "right";
    },
    showDivisionFilter(){
      return this.$store.state.admin.user.info.division_id;
    }
  },
  created() {
    this.getDivisionOption();
    this.getOrderList();
    //
  },
  methods: {
    getDivisionOption(){
      getDivisionOptionApi().then(res=>{
        this.divisionList = res.data;
      })
    },
    getDivisionAgentOption(){
      getDivisionAgentOptionApi(this.pagination.division_id).then(res=>{
        this.divisionAgentList = res.data;
        console.log(res.data);
      })
    },
    agentSearch(){
      this.getDivisionAgentOption();
      this.pagination.page = 1;
      this.getOrderList();
    },
    search() {
      this.pagination.page = 1;
      this.getOrderList();
    },
    // 具体日期搜索()；
    onchangeTime(e) {
      this.pagination.page = 1;
      this.timeVal = e;
      this.pagination.time = this.timeVal[0] ? this.timeVal.join("-") : "";
    },

    // 订单列表
    getOrderList() {
      this.loading = true;
      getDivisionOrder(this.pagination)
        .then((res) => {
          const { count, data, num } = res.data;
          this.orderList = data;
          this.total = count;
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          this.$Message.error(err.msg);
        });
    },
    clearTap(e) {
      this.pagination.page = 1;
      this.getOrderList();
    },
    // 分页
    pageChange(index) {
      this.pagination.page = index;
      this.getOrderList();
    },
    nameSearch() {
      this.pagination.page = 1;
      this.getOrderList();
    },
    async exports() {
      let [th, filekey, data, fileName] = [[], [], [], ""];
      //   let fileName = "";
      let excelData = JSON.parse(JSON.stringify(this.pagination));
      excelData.page = 1;
      excelData.limit = 100;
      for (let i = 0; i < excelData.page + 1; i++) {
        let lebData = await this.getExcelData(excelData);
        if (!fileName) fileName = lebData.filename;
        if (!filekey.length) {
          filekey = lebData.filekey;
        }
        if (!th.length) th = lebData.header;
        if (lebData.export.length) {
          data = data.concat(lebData.export);
          excelData.page++;
        } else {
          exportExcel(th, filekey, fileName, data);
          return;
        }
      }
    },
    getExcelData(excelData) {
      return new Promise((resolve, reject) => {
        getDivisionOrderExportApi(excelData).then((res) => {
          return resolve(res.data);
        });
      });
    },
    //getDivisionOrderExportApi
  },
};
</script>

<style lang="stylus" scoped>
.span-del {
 color: #ed4014;
 display: block
}
.code {
  position: relative;
}

.QRpic {
  width: 180px;
  height: 259px;

  img {
    width: 100%;
    height: 100%;
  }
}

.tabBox {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;

  .tabBox_img {
    width: 30px;
    height: 30px;

    img {
      width: 100%;
      height: 100%;
    }
  }

  .tabBox_tit {
    width:245px;
    height:30px;
    line-height:30px;
    font-size: 12px !important;
    margin: 0 2px 0 10px;
    letter-spacing: 1px;
    box-sizing: border-box;
  }
}

.tabBox +.tabBox{
  margin-top:5px;
}

.pictrue-box {
  display: flex;
  align-item: center;
}

.pictrue {
  width: 25px;
  height: 25px;
}
.tdinfo{
  margin-left: 75px;
  margin-top: 16px;
}
.expand-row{
  margin-bottom: 16px;
  font-size: 12px;
}
/deep/.vxe-table--render-default .vxe-cell{
  font-size: 12px;
}
</style>
