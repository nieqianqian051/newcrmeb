<template>
  <div>
    <!-- 商品信息-->
    <FormItem label="商品类型：" props="is_virtual">
      <div
        class="productType"
        :class="formValidate.product_type == item.id ? 'on' : ''"
        v-for="(item, index) in productType"
        :key="index"
        @click="productTypeTap(1, item)"
      >
        <div class="name">{{ item.name }}</div>
        <div class="title">({{ item.title }})</div>
        <div v-if="formValidate.product_type == item.id" class="jiao"></div>
        <div
          v-if="formValidate.product_type == item.id"
          class="iconfont iconduihao"
        ></div>
      </div>
    </FormItem>
    <FormItem label="商品名称：" prop="store_name">
      <Input
        v-model="formValidate.store_name"
        placeholder="请输入商品名称"
        v-width="'50%'"
      />
    </FormItem>
    <FormItem label="商品分类：" prop="cate_id">
      <el-cascader
        placeholder="请选择商品分类"
        v-width="'50%'"
        size="mini"
        v-model="formValidate.cate_id"
        :options="treeSelect"
        :props="props"
        filterable
        clearable
      >
      </el-cascader>
      <span class="addClass" @click="addClass">新增分类</span>
    </FormItem>
    <FormItem label="商品品牌：" prop="">
      <div class="flex">
        <Cascader
          :data="brandData"
          placeholder="请选择商品品牌"
          change-on-select
          v-model="formValidate.brand_id"
          filterable
          v-width="'50%'"
        ></Cascader>
        <span class="addClass" @click="addBrand">新增品牌</span>
      </div>
    </FormItem>
    <FormItem label="单位：" prop="unit_name">
      <Select
        v-model="formValidate.unit_name"
        clearable
        filterable
        v-width="'50%'"
        placeholder="请输入单位"
      >
        <Option
          v-for="(item, index) in unitNameList"
          :value="item.name"
          :key="index"
          >{{ item.name }}</Option
        >
      </Select>
      <span class="addClass" @click="addUnit">新增单位</span>
    </FormItem>
    <FormItem label="商品编码：" prop="">
      <Input
        v-model="formValidate.code"
        placeholder="请输入商品编码"
        v-width="'50%'"
      />
    </FormItem>
    <FormItem label="商品轮播图：" prop="slider_image">
      <div class="acea-row">
        <div
          class="pictrue"
          v-for="(item, index) in formValidate.slider_image"
          :key="index"
          draggable="true"
          @dragstart="handleDragStart($event, item)"
          @dragover.prevent="handleDragOver($event, item)"
          @dragenter="handleDragEnter($event, item)"
          @dragend="handleDragEnd($event, item)"
        >
          <img v-lazy="item" />
          <Button
            shape="circle"
            icon="md-close"
            @click.native="handleRemove(index)"
            class="btndel"
          ></Button>
        </div>
        <div
          v-if="formValidate.slider_image.length < 10"
          class="upLoad acea-row row-center-wrapper"
          @click="modalPicTap('duo')"
        >
          <Icon type="ios-camera-outline" size="26" />
        </div>
        <Input
          v-model="formValidate.slider_image[0]"
          class="input-display"
        ></Input>
      </div>
      <div class="tips">
        建议尺寸：800 *
        800px，可拖拽改变图片顺序，默认首张图为主图，最多上传10张
      </div>
    </FormItem>
    <FormItem label="商品标签：" prop="store_label_id" class="labelClass">
      <div class="acea-row row-middle">
        <div
          class="labelInput acea-row row-between-wrapper"
          @click="openStoreLabel"
        >
          <div style="width: 90%;">
            <div v-if="formValidate.store_label_id.length">
              <Tag
                closable
                v-for="(item, index) in formValidate.store_label_id"
                :key="index"
                @on-close="closeStoreLabel(item)"
                >{{ item.label_name }}</Tag
              >
            </div>
            <span class="span" v-else>选择商品标签</span>
          </div>
          <div class="iconfont iconxiayi"></div>
        </div>
        <span class="addClass" @click="addStoreLabel">新增标签</span>
      </div>
    </FormItem>
    <FormItem label="添加视频：">
      <i-switch v-model="formValidate.video_open" size="large">
        <span slot="open">开启</span>
        <span slot="close">关闭</span>
      </i-switch>
    </FormItem>
    <FormItem
      label="上传视频："
      prop="video_link"
      v-if="formValidate.video_open"
    >
      <div class="flex">
        <Input v-model="formValidate.video_link" v-width="'50%'" />
        <span class="addClass" @click="addStoreLabel">选择视频</span>
      </div>
      <div class="iview-video-style" v-if="formValidate.video_link">
        <video
          class="video-style"
          :src="formValidate.video_link"
          controls="controls"
        ></video>
        <div class="mark"></div>
        <Icon type="ios-trash-outline" class="iconv" @click="delVideo" />
      </div>
    </FormItem>
    <FormItem label="上架时间：">
      <RadioGroup v-model="formValidate.is_show" @on-change="goodsOn">
        <Radio :label="1">
          <Icon type="social-apple"></Icon>
          <span>立即上架</span>
        </Radio>
        <Radio :label="2">
          <Icon type="social-android"></Icon>
          <span>定时上架</span>
        </Radio>
        <Radio :label="0">
          <Icon type="social-windows"></Icon>
          <span>放入仓库</span>
        </Radio>
      </RadioGroup>
    </FormItem>
    <FormItem label="" v-if="formValidate.is_show == 2">
      <DatePicker
        type="datetime"
        @on-change="onchangeShow"
        :options="startPickOptions"
        :value="formValidate.auto_on_time"
        v-model="formValidate.auto_on_time"
        placeholder="请选择上架时间"
        format="yyyy-MM-dd HH:mm"
        style="width: 250px;"
      ></DatePicker>
    </FormItem>
    <FormItem label="定时下架：">
      <Switch
        v-model="formValidate.off_show"
        :true-value="1"
        :false-value="0"
        size="large"
        @on-change="goodsOff"
      >
        <span slot="open">开启</span>
        <span slot="close">关闭</span>
      </Switch>
    </FormItem>
    <FormItem label="" v-if="formValidate.off_show == 1">
      <DatePicker
        type="datetime"
        @on-change="onchangeOff"
        :options="endPickOptions"
        :value="formValidate.auto_off_time"
        v-model="formValidate.auto_off_time"
        placeholder="请选择下架时间"
        format="yyyy-MM-dd HH:mm"
        style="width: 260px;"
      ></DatePicker>
      <div class="tips">
        开启定时下架后，系统会在设置时间下架该商品。下架时间需晚于开售时间，商品才能定时开售。
      </div>
    </FormItem>

    <!-- 商品标签 -->
    <Modal
      v-model="storeLabelShow"
      scrollable
      title="选择商品标签"
      :closable="true"
      width="540"
      :footer-hide="true"
      :mask-closable="false"
    >
      <storeLabelList
        ref="storeLabel"
        @activeData="activeStoreData"
        @close="storeLabelClose"
      ></storeLabelList>
    </Modal>
  </div>
</template>
<script>
import productMixin from "../mixins/index.js";
import {
  cascaderListApi,
  productCreateApi,
  brandList,
  productAllUnit,
  productUnitCreate,
  productLabelAdd,
} from "@/api/product";
import storeLabelList from "@/components/storeLabelList";
import vuedraggable from "vuedraggable";
export default {
  name: "productBaseSet",
  props: {
    baseInfo: {
      type: Object,
      default: () => {},
    },
  },
  data() {
    return {
      formValidate: {
        brand_id: [],
        code: "",
        product_type: 0,
        slider_image: [],
        store_name: "",
        cate_id: [],
        store_label_id: [],
        unit_name: "",
        video_link: "",
        video_open: false,
        is_show: 0,
        auto_on_time: "",
        auto_off_time: "",
        off_show: 0,
      },
      productType: [
        { name: "普通商品", title: "物流发货", id: 0 },
        { name: "卡密/网盘", title: "自动发货", id: 1 },
        { name: "虚拟商品", title: "虚拟发货", id: 3 },
        { name: "次卡商品", title: "到店核销", id: 4 },
      ],
      props: { emitPath: false, multiple: true, checkStrictly: true },
      //商品分类树形数据
      treeSelect: [],
      // 品牌数据
      brandData: [],
      // 单位数据
      unitNameList: [],
      storeLabelShow: false,
    };
  },
  components: {
    storeLabelList,
    draggable: vuedraggable,
  },
  mixins: [productMixin],
  watch: {
    baseInfo: {
      handler(val) {
        let keys = Object.keys(this.formValidate);
        keys.map((i) => {
          this.formValidate[i] = val[i];
        });
      },
      deep: true,
      immediate: true,
    },
  },
  created() {
    this.goodsCategory();
    this.getBrandList();
    this.getAllUnit();
  },
  methods: {
    productTypeTap(num, item) {
      if (num == 1) {
        if (this.$route.params.id) return this.$Message.error("商品类型不能切换！");
        this.formValidate.product_type = item.id;
      }
      if (this.formValidate.product_type) {
        this.headTab = [
          { title: "基础信息", name: "1" },
          { title: "规格库存", name: "2" },
          { title: "商品详情", name: "3" },
          { title: "营销设置", name: "5" },
          { title: "其他设置", name: "6" },
        ];
        this.formValidate.postage = 0;
        this.formValidate.supplier_id = 0;
      } else {
        this.headTab = [
          { title: "基础信息", name: "1" },
          { title: "规格库存", name: "2" },
          { title: "商品详情", name: "3" },
          { title: "物流设置", name: "4" },
          { title: "营销设置", name: "5" },
          { title: "其他设置", name: "6" },
        ];
      }
    },
    // 品牌列表
    getBrandList() {
      brandList()
        .then((res) => {
          //initBran()函数作用iview中规定value必须是字符串，后台返回成了数字，用于处理这个，给了个递归；
          this.initBran(res.data);
          this.brandData = res.data;
        })
        .catch((err) => {
          this.$Message.error(err.msg);
        });
    },
    initBran(data) {
      data.map((item) => {
        item.value = item.value.toString();
        if (item.children && item.children.length) {
          this.initBran(item.children);
        }
      });
    },
    addBrand() {},
    // 商品分类；
    goodsCategory() {
      cascaderListApi(1)
        .then((res) => {
          this.treeSelect = res.data;
        })
        .catch((res) => {
          this.$Message.error(res.msg);
        });
    },
    addClass() {
      this.$modalForm(productCreateApi()).then(() => this.goodsCategory());
    },
    getAllUnit() {
      productAllUnit()
        .then((res) => {
          this.unitNameList = res.data;
        })
        .catch((err) => {
          this.$Message.error(err.msg);
        });
    },
    addUnit() {
      this.$modalForm(productUnitCreate()).then(() => this.getAllUnit());
    },
    addStoreLabel() {
      this.$modalForm(productLabelAdd()).then(() => {});
    },
    activeStoreData(storeDataLabel) {
      this.storeLabelShow = false;
      this.formValidate.store_label_id = storeDataLabel;
    },
    openStoreLabel(row) {
      this.storeLabelShow = true;
      this.$refs.storeLabel.storeLabel(
        JSON.parse(JSON.stringify(this.formValidate.store_label_id))
      );
    },
    // 标签弹窗关闭
    storeLabelClose() {
      this.storeLabelShow = false;
    },
    goodsOn(e) {
      if (e == 0 || e == 1) {
        this.formValidate.auto_on_time = "";
      }
    },
    goodsOff(e) {
      if (!e) {
        this.formValidate.auto_off_time = "";
      }
    },
    //定时上架
    onchangeShow(e) {
      this.formValidate.auto_on_time = e;
    },
    //定时下架
    onchangeOff(e) {
      this.formValidate.auto_off_time = e;
    },
    // 删除视频；
    delVideo() {
      this.$set(this.formValidate, "video_link", "");
    },
    // 移动
    handleDragStart(e, item) {
      this.dragging = item;
    },
    handleDragEnd(e, item) {
      this.dragging = null;
    },
    handleDragOver(e) {
      e.dataTransfer.dropEffect = "move";
    },
    handleDragEnter(e, item) {
      e.dataTransfer.effectAllowed = "move";
      if (item === this.dragging) {
        return;
      }
      const newItems = [...this.formValidate.slider_image];
      const src = newItems.indexOf(this.dragging);
      const dst = newItems.indexOf(item);
      newItems.splice(dst, 0, ...newItems.splice(src, 1));
      this.formValidate.slider_image = newItems;
    },
    handleRemove(i) {
      this.formValidate.slider_image.splice(i, 1);
    },
    modalPicTap() {
      this.$imgModal((e) => {
        console.log(e);
      });
    },
  },
};
</script>
<style scoped lang="less">
.productType {
  width: 120px;
  height: 60px;
  background: #ffffff;
  border-radius: 3px;
  border: 1px solid #e7e7e7;
  float: left;
  text-align: center;
  padding-top: 8px;
  position: relative;
  cursor: pointer;
  line-height: 23px;
  margin-right: 12px;

  &.on {
    border-color: #1890ff;
  }

  .name {
    font-size: 14px;
    font-weight: 600;
    color: rgba(0, 0, 0, 0.85);
  }

  .title {
    font-size: 12px;
    font-weight: 400;
    color: #999999;
  }

  .jiao {
    position: absolute;
    bottom: 0;
    right: 0;
    width: 0;
    height: 0;
    border-bottom: 26px solid #1890ff;
    border-left: 26px solid transparent;
  }

  .iconfont {
    position: absolute;
    bottom: -3px;
    right: 1px;
    color: #ffffff;
    font-size: 12px;
  }
}
.addClass {
  color: #1890ff;
  margin-left: 14px;
  cursor: pointer;
}
.pictrue {
  width: 60px;
  height: 60px;
  border: 1px dotted rgba(0, 0, 0, 0.1);
  margin-right: 15px;
  margin-bottom: 10px;
  display: inline-block;
  position: relative;
  cursor: pointer;

  img {
    width: 100%;
    height: 100%;
  }

  .btndel {
    position: absolute;
    z-index: 1;
    width: 20px !important;
    height: 20px !important;
    left: 46px;
    top: -4px;
  }
}

.upLoad {
  width: 58px;
  height: 58px;
  line-height: 58px;
  border: 1px dotted rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  background: rgba(0, 0, 0, 0.02);
  cursor: pointer;
}
.input-display {
  display: none;
}
.labelInput {
  border: 1px solid #dcdee2;
  width: 50%;
  padding: 0 5px;
  border-radius: 5px;
  min-height: 30px;
  cursor: pointer;
  .span {
    color: #c5c8ce;
  }
  .iconxiayi {
    font-size: 12px;
  }
}
.labelClass {
  /deep/.ivu-form-item-content {
    line-height: unset;
  }
}
.iview-video-style {
  width: 40%;
  height: 180px;
  border-radius: 10px;
  background-color: #707070;
  margin-top: 10px;
  position: relative;
  overflow: hidden;
}

.iview-video-style .iconv {
  color: #fff;
  line-height: 180px;
  width: 50px;
  height: 50px;
  display: inherit;
  font-size: 26px;
  position: absolute;
  top: -74px;
  left: 50%;
  margin-left: -25px;
  cursor: pointer;
}

.iview-video-style .mark {
  position: absolute;
  width: 100%;
  height: 30px;
  top: 0;
  background-color: rgba(0, 0, 0, 0.5);
  text-align: center;
}
.video-style {
  width: 100%;
  height: 100% !important;
  border-radius: 10px;
}
</style>
