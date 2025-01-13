<template>
  <Modal
    v-model="visible"
    width="1024px"
    scrollable
    footer-hide
    closable
    title="选择图片"
    :mask-closable="false"
    :z-index="1"
  >
    <uploadPictures
      v-if="visible"
      :isChoice="isChoice"
      @getPicD="getImage"
      :gridBtn="gridBtn"
      :gridPic="gridPic"
    ></uploadPictures>
  </Modal>
</template>
<script>
import uploadPictures from './index.vue';
export default {
  name: '',
  components: { uploadPictures },
  data() {
    return {
      more: false,
      isChoice: '',
      visible: false,
      callback: function () {},
      gridBtn: {
        xl: 4,
        lg: 8,
        md: 8,
        sm: 8,
        xs: 8,
      },
      gridPic: {
        xl: 6,
        lg: 8,
        md: 12,
        sm: 12,
        xs: 12,
      },
      more: false,
    };
  },
  computed: {
    isMore() {
      return this.more ? '多选' : '单选';
    },
  },
  methods: {
    handleClose() {
      this.visible = false;
      this.callback(this.visible);
    },
    getImage(img) {
      this.callback(img);
      this.visible = false;
    },
  },
};
</script>
<style lang="scss" scoped></style>
