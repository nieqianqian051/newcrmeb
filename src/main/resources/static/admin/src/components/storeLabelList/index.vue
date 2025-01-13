<template>
  <div class="label-wrapper">
    <div class="list-box">
      <div
        class="label-box"
        v-for="(item, index) in labelList"
        :key="index"
        v-if="isStore"
      >
        <div class="title mb-10" v-if="item.children && item.children.length">
          {{ item.label_name }}
        </div>
        <div class="list" v-if="item.children && item.children.length">
          <div
            v-for="(label, j) in item.children"
            :key="j"
            class="relative label-pro acea-row row-center-wrapper"
            :class="{'active-label': label.disabled}"
            @click="selectLabel(label)"
          >
            <div
              class="label-item"
              :style="{
                backgroundColor: label.bg_color,
                color: label.color,
                border: label.border_color
                  ? '1px solid ' + label.border_color
                  : 'none',
              }"
              v-if="!label.icon"
            >
              {{ label.label_name }}
            </div>
            <img :src="label.icon" class="img-tag" v-else />
            <div class="sanjiao" v-show="label.disabled">
              <span class="iconfont iconwancheng"></span>
            </div>
          </div>
        </div>
      </div>
      <div v-if="!isStore">暂无标签</div>
    </div>
    <div class="footer">
      <Button @click="cancel">取消</Button>
      <Button type="primary" class="ml14" @click="subBtn">确定</Button>
    </div>
  </div>
</template>

<script>
import { productStoreLabel } from "@/api/product";

export default {
  name: "storeLabelList",
  props: {},
  data() {
    return {
      labelList: [],
      dataLabel: [],
      isStore: false,
    };
  },
  mounted() {},
  methods: {
    inArray: function(search, array) {
      for (let i in array) {
        if (array[i].id == search) {
          return true;
        }
      }
      return false;
    },
    // 用户标签
    storeLabel(data) {
      this.dataLabel = data;
      productStoreLabel()
        .then((res) => {
          res.data.map((el) => {
            if (el.children && el.children.length) {
              this.isStore = true;
              el.children.map((label) => {
                if (this.inArray(label.id, this.dataLabel)) {
                  label.disabled = true;
                } else {
                  label.disabled = false;
                }
              });
            }
          });
          this.labelList = res.data;
        })
        .catch((res) => {
          this.$Message.error(res.msg);
        });
    },
    selectLabel(label) {
      if (label.disabled) {
        let index = this.dataLabel.indexOf(
          this.dataLabel.filter((d) => d.id == label.id)[0]
        );
        this.dataLabel.splice(index, 1);
        label.disabled = false;
      } else {
        this.dataLabel.push({ label_name: label.label_name, id: label.id });
        label.disabled = true;
      }
    },
    // 确定
    subBtn() {
      this.$emit("activeData", JSON.parse(JSON.stringify(this.dataLabel)));
    },
    cancel() {
      this.$emit("close");
    },
  },
};
</script>

<style lang="stylus" scoped>
.label-wrapper
  .list
    display: flex;
    flex-wrap: wrap;
    .label-pro{
      border: 1px solid #FFFFFF;
      padding: 2px;
      border-radius: 4px;
      margin: 0 8px 10px 0;
      cursor: pointer;
    }
    .active-label{
      border: 1px solid #2d8cf0;
    }
    .label-item {
      padding: 2px 8px;
      background: #EEEEEE;
      color: #333333;
      border-radius: 2px;
      font-size: 12px;
    }
    .sanjiao{
      position: absolute;
      right: 0;
      bottom: 0;
      width: 20px;
      height: 20px;
      background: #2d8cf0;
      clip-path: polygon(100% 100%, 100% 0, 0 100%);
      color: #fff;
      text-align: right;
      .iconfont{
        font-size: 10px;
      }
    }
  .footer
    display flex
    justify-content flex-end
    margin-top 40px

    button
      margin-left 10px

.btn
  width 60px
  height 24px

.title
  font-size 13px

.list-box
  overflow-y auto
  overflow-x hidden
  max-height 340px

  &::-webkit-scrollbar {
    width: 0;
  }

.img-tag {
  height: 22px;
  border-radius: 2px;
}
</style>
