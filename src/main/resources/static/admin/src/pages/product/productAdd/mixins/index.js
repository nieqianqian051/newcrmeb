import { mapState, mapMutations } from "vuex";
export default {
  data() {
    return {
      ruleValidate: {
        store_name: [
          { required: true, message: "请输入商品名称", trigger: "blur" },
        ],
        cate_id: [
          {
            required: true,
            message: "请选择商品分类",
            trigger: "change",
            type: "array",
          },
        ],
        keyword: [
          { required: true, message: "请输入商品关键字", trigger: "blur" },
        ],
        unit_name: [
          {
            required: true,
            message: "请输入单位",
            trigger: "change",
          },
        ],
        store_info: [
          { required: true, message: "请输入商品简介", trigger: "blur" },
        ],
        slider_image: [
          {
            required: true,
            message: "请上传商品轮播图",
            type: "array",
          },
        ],
        spec_type: [
          { required: true, message: "请选择商品规格", trigger: "change" },
        ],
        selectRule: [
          { required: true, message: "请选择商品规格属性", trigger: "change" },
        ],
        give_integral: [{ type: "integer", message: "请输入整数" }],
      },
    };
  },
  computed: {
    ...mapState("admin/layout", ["isMobile", "menuCollapse"]),
    startPickOptions() {
      const that = this;
      return {
        disabledDate(time) {
          if (that.formValidate.auto_off_time) {
            return (
              time.getTime() >
              new Date(that.formValidate.auto_off_time).getTime()
            );
          }
          return "";
        },
      };
    },
    endPickOptions() {
      const that = this;
      return {
        disabledDate(time) {
          if (that.formValidate.is_show == "1") {
            return time.getTime() < Date.now();
          }
          if (that.formValidate.auto_on_time) {
            return (
              time.getTime() <
              new Date(that.formValidate.auto_on_time).getTime()
            );
          }
          return "";
        },
      };
    },
  },
  methods: {
    
  },
};
