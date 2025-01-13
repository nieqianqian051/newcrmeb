<template>
  <div class="article-manager video-icon form-submit" id="shopp-manager">
    <div class="i-layout-page-header">
      <PageHeader class="product_tabs" hidden-breadcrumb>
        <div slot="title" class="acea-row row-middle">
          <router-link :to="{ path: '/admin/setting/document' }">
            <div class="font-sm after-line">
              <span class="iconfont iconfanhui"></span>
              <span class="pl10">返回</span>
            </div>
          </router-link>
          <span class="mr20 ml16">小票配置</span>
        </div>
      </PageHeader>
    </div>
    <Card :bordered="false" dis-hover class="ivu-mt">
      <div class="flex justify-between warpper">
        <Form :model="formItem" :label-width="120">
          <FormItem label="小票头部：">
            <Checkbox
              v-model="formItem.header"
              :true-value="1"
              :false-value="0"
              >商家名称</Checkbox
            >
          </FormItem>
          <FormItem label="配送信息：">
            <Checkbox
              v-model="formItem.delivery"
              :true-value="1"
              :false-value="0"
              >配送信息</Checkbox
            >
          </FormItem>
          <FormItem label="买家备注：">
            <Checkbox
              v-model="formItem.buyer_remarks"
              :true-value="1"
              :false-value="0"
              >买家备注</Checkbox
            >
          </FormItem>
          <FormItem label="商品信息：">
            <CheckboxGroup v-model="formItem.goods">
              <Checkbox :label="0">商品基础信息</Checkbox>
              <Checkbox :label="1" :disabled="!formItem.goods.includes(0)">规格编码</Checkbox>
            </CheckboxGroup>
          </FormItem>
          <FormItem label="运费信息：">
            <Checkbox
              v-model="formItem.freight"
              :true-value="1"
              :false-value="0"
              >运费</Checkbox
            >
          </FormItem>
          <FormItem label="优惠信息：">
            <Checkbox
              v-model="formItem.preferential"
              :true-value="1"
              :false-value="0"
              >优惠总计</Checkbox
            >
          </FormItem>
          <FormItem label="支付信息：">
            <CheckboxGroup v-model="formItem.pay">
              <Checkbox :label="0">支付方式</Checkbox>
              <Checkbox :label="1">实收金额</Checkbox>
            </CheckboxGroup>
          </FormItem>
          <FormItem label="其他订单信息：">
            <CheckboxGroup v-model="formItem.order">
              <Checkbox :label="0">订单编号</Checkbox>
              <Checkbox :label="1">下单时间</Checkbox>
              <Checkbox :label="2">支付时间</Checkbox>
              <Checkbox :label="3">打印时间</Checkbox>
            </CheckboxGroup>
          </FormItem>
          <FormItem label="推广二维码：">
            <Checkbox v-model="formItem.code" :true-value="1" :false-value="0"
              >选择系统链接</Checkbox
            >
            <div v-if="formItem.code" class="link">
              <div class="input-box">
                链接：{{ formItem.code_url }}
                <span class="change" @click="getLink(index)">{{
                  formItem.code_url ? "修改" : "选择"
                }}</span>
              </div>
            </div>
          </FormItem>
          <FormItem label="底部公告：">
            <Checkbox
              v-model="formItem.show_notice"
              :true-value="1"
              :false-value="0"
              >底部公告</Checkbox
            >
            <div v-if="formItem.show_notice">
              <Input
                v-model="formItem.notice_content"
                maxlength="50"
                show-word-limit
                type="textarea"
                placeholder="请输入公告内容"
                style="width: 500px"
              />
            </div>
          </FormItem>
        </Form>
        <div class="ticket-preview">
          <div class="out-line"></div>
          <div class="ticket-content">
            <div v-if="formItem.header === 1" class="ticket-header">
              商家名称
            </div>
            <!-- 配送方式 -->
            <div class="delivery btn-line" v-show="formItem.delivery">
              <div class="form-box">
                <div class="label">配送方式：</div>
                <div class="content">商家配送</div>
              </div>
              <div class="form-box">
                <div class="label">客户姓名：</div>
                <div class="content">收货人姓名</div>
              </div>
              <div class="form-box">
                <div class="label">客户电话：</div>
                <div class="content">13023354455</div>
              </div>
              <div class="form-box">
                <div class="label">收货地址：</div>
                <div class="content">上海市浦东新区世界大道25号B座309室</div>
              </div>
            </div>
            <!-- 备注 -->
            <div class="buyer-remarks btn-line" v-show="formItem.buyer_remarks">
              <div class="form-box">
                <div class="label">买家备注：</div>
                <div class="content">请在收货时向商家留言，谢谢！</div>
              </div>
            </div>
            <!-- 商品 -->
            <div class="goods btn-line" v-show="formItem.goods.includes(0)">
              <div class="star-line">
                *******************商品*******************
              </div>
              <div class="flex justify-between">
                <span>商品</span>
                <span>单价</span>
                <span>数量</span>
                <span>金额</span>
              </div>
            </div>
            <div class="goods-msg btn-line" v-show="formItem.goods.includes(0)">
              <div class="flex justify-between">
                <span>商品1</span>
                <span>100.0</span>
                <span>2</span>
                <span>200.0</span>
              </div>
              <div class="flex justify-between">
                <span>(规格1)</span>
                <span></span>
                <span></span>
                <span></span>
              </div>
              <div v-if="formItem.goods.includes(1)" class="flex py-10">
                <span>规格编码：</span>
                <span>FKXQW4567vw50</span>
              </div>
            </div>
            <div class="goods-msg pb-10 pt-10" v-show="formItem.goods.includes(0)">
              <div class="flex justify-between">
                <span>商品2</span>
                <span>100.0</span>
                <span>2</span>
                <span>200.0</span>
              </div>
              <div class="flex justify-between">
                <span>(规格2)</span>
                <span></span>
                <span></span>
                <span></span>
              </div>
              <div v-if="formItem.goods.includes(1)" class="flex py-10">
                <span>规格编码：</span>
                <span>FKXQW4567vw50</span>
              </div>
            </div>
            <div class="star-line" v-show="formItem.goods.includes(0)">
              ******************************************
            </div>
            <!-- 运费 -->
            <div class="pay flex flex-col align-end btn-line" v-show="formItem.freight">
              <template>
                <div>运费：10.00元</div>
                <div class="fw-500">合计：410.00元</div>
              </template>
            </div>
            <!-- 优惠 -->
            <div class="pay flex flex-col align-end btn-line" v-show="formItem.preferential">
              <template>
                <div>优惠：-80.00元</div>
                <div>抵扣：-20.00元</div>
              </template>
            </div>
            <!-- 支付信息 -->

            <div class="pay flex flex-col align-end btn-line" v-show="formItem.pay.length">
              <div v-show="formItem.pay.includes(0)">支付方式：微信支付</div>
              <div v-show="formItem.pay.includes(1)" class="fw-500">实际支付：310.00元</div>
            </div>
            <!-- 订单信息 -->

            <div class="order pt-10 btn-line" v-show="formItem.order.length">
              <div v-show="formItem.order.includes(0)">订单编号：wx1234567890</div>
              <div v-show="formItem.order.includes(1)">下单时间：2024/09/23 12:00:00</div>
              <div v-show="formItem.order.includes(2)">
                支付时间：2024/09/23 12:00:00
              </div>
              <div v-show="formItem.order.includes(3)">
                打印时间：2024/09/23 12:00:00
              </div>
            </div>
            <!-- 二维码 -->
            <div class="code">
              <div v-show="formItem.code" id="qrcode"></div>
              <div class="mt-20" v-if="formItem.show_notice">
                {{ formItem.notice_content }}
              </div>
            </div>
          </div>
          <div class="bottom-notice">
            <img class="image" src="@/assets/images/p-btn.png" alt="" />
          </div>
        </div>
      </div>
    </Card>
    <Card :bordered="false" dis-hover class="fixed-card">
      <Button type="primary" class="submission" @click="save">保存</Button>
    </Card>
    <linkaddress ref="linkaddres" @linkUrl="linkUrl"></linkaddress>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import { printContent, printSaveContent } from "@/api/setting";
import linkaddress from "@/components/linkaddress";
import QRCode from "qrcodejs2";
import Setting from "@/setting";
export default {
  name: "content",
  components: { linkaddress },
  data() {
    return {
      formItem: {
        header: 1,
        delivery: 1,
        buyer_remarks: 1,
        goods: [0],
        freight: 1,
        preferential: 1,
        pay: [0, 1],
        order: [0, 1],
        code: 0,
        code_url: "",
        show_notice: 0,
        notice_content: "",
      },
      code: "",
      BaseURL: Setting.apiBaseURL.replace(/adminapi/, ""),
      id: this.$route.query.id,
    };
  },
  computed: {
    ...mapState("admin/layout", ["isMobile", "menuCollapse"]),
    labelWidth() {
      return this.isMobile ? undefined : 120;
    },
    labelPosition() {
      return this.isMobile ? "top" : "right";
    },
    labelBottom() {
      return this.isMobile ? undefined : 15;
    },
  },
  created() {
    if (this.id) this.getPrintContent();
  },
  methods: {
    getPrintContent() {
      printContent(this.id).then((res) => {
        if (!Array.isArray(res.data)) this.formItem = res.data;
        if (res.data.code && res.data.code_url) {
          this.code = this.BaseURL + res.data.code_url;
          this.$nextTick((e) => {
            this.drawCode(this.code);
          });
        }
      });
    },
    save() {
      printSaveContent(this.id, this.formItem)
        .then((res) => {
          this.$Message.success("保存成功");
        })
        .catch((err) => {
          this.$Message.error("保存失败");
        });
    },
    getLink(index) {
      this.$refs.linkaddres.modals = true;
    },
    linkUrl(e) {
      this.formItem.code_url = e;
      let url = this.BaseURL + e;
      this.drawCode(url);
    },
    drawCode(url) {
      let qrcode = "";
      let obj = document.getElementById("qrcode");
      obj.innerHTML = "";
      qrcode = new QRCode(obj, {
        text: url, // 需要转换为二维码的内容
        width: 128,
        height: 128,
        colorDark: "#000000",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.H,
      });
    },
  },
};
</script>
<style scoped lang="stylus">
/deep/ .ivu-checkbox-wrapper{
	font-size 12px;
    margin-right 30px
}
/deep/ .ivu-checkbox{
    margin-right 6px
}
/deep/ .ivu-checkbox-inner{
    width 14px;
    height: 14px
    font-size: 12px
}
/deep/ .ivu-checkbox-checked .ivu-checkbox-inner:after{
    top: 1px;
    left: 4px;
}
/deep/.ivu-card{
    border-radius: 0;
	font-size inherit;

}
.warpper{
    max-width: 1200px;
}
.fixed-card {
    position: fixed;
    right: 0;
    bottom: 0;
    left: 200px;
    z-index: 45;
    box-shadow: 0 -1px 2px rgb(240, 240, 240);

    /deep/ .ivu-card-body {
        padding: 15px 16px 14px;
        text-align: center;
    }

    .ivu-form-item {
        margin-bottom: 0;
    }

    /deep/ .ivu-form-item-content {
        margin-right: 124px;
        text-align: center;
    }

    .ivu-btn {
        height: 36px;
        padding: 0 20px;
    }
}
    .link{
        background: #F6F7F9;
        border-radius: 2px;
        padding 20px
    }
    .change{
        color: #2D8CF0;
        cursor pointer
    }
// 隐藏滚动条
.ticket-content::-webkit-scrollbar {
    display: none;
}
.ticket-preview {
    display flex
    flex-direction: column
    align-items: center
}
.out-line{
    width: 271px;
    height: 7px;
    background: #EEEEEE;
    border-radius: 4px;
}
// 动画高度从0变为100%
@keyframes show {
    0% {
        margin-top: -70vh;
    }
    100% {
        margin-top: 0;
    }
}
.ticket-preview{
    overflow hidden;
    height: 70vh;
}
.ticket-content{
    position relative
    top: -3px;
    animation show 2s ease-in-out forwards;
    width: 260px;
    max-height: 70vh;
    overflow-y: scroll
    overflow-x: hidden
    background-color: #fff;
    padding: 20px 15px 15px 15px;
    box-shadow: 0px 4px 10px 0px rgba(0,0,0,0.1);
    border-radius: 1px 1px 1px 1px;
    font-size: 12px;
    font-weight: 400;
    color #333;
    line-height: 18px;
    .form-box{
        display: flex;
        .label{
            white-space: nowrap
        }
    }
    .ticket-header{
        font-weight: 500;
        font-size: 18px;
        text-align: center;
        margin-bottom: 20px;
    }
    // 下划线虚线
    .btn-line{
        border-bottom: 1px dashed #eee;
        padding 10px 0
    }
    .star-line{
      font-family: "Microsoft YaHei";
      font-size: 12px;
      display: flex;
      justify-content: center;
      overflow: hidden;
      white-space: nowrap;
    }
    .fw-500{
        font-weight: 500;
    }
    .code{
        display flex
        flex-direction: column
        align-items: center

        text-align center
        #qrcode{
            margin: 25px 0 0px
        }
    }


}
 .bottom-notice{
    width: 260px;
    margin-left 1px
    height 13px
    position: relative;
}
.image {
    width: 100%;
    height 100%
    position absolute
    top -6px;
}
</style>
