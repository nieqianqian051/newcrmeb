<template>
  <div>
    <div class="i-layout-page-header header-title">
      <span class="ivu-page-header-title">{{ $route.meta.title }}</span>
    </div>
    <Card :bordered="false" shadow="never" class="ivu-mt">
      <Form label-width="85px" @submit.native.prevent v-loading="spinShow">
        <FormItem label="协议内容：">
          <WangEditor :content="agreement.content" @editorContent="getEditorContent"></WangEditor>
        </FormItem>
        <FormItem>
          <Button type="primary" v-db-click @click="memberAgreementSave">保存</Button>
        </FormItem>
      </Form>
    </Card>
  </div>
</template>

<script>
import WangEditor from '@/components/wangEditor/index.vue';
import { agentAgreement, agentAgreementSave } from '@/api/user';

export default {
  components: { WangEditor },
  data() {
    return {
      ueConfig: {
        autoHeightEnabled: false,
        initialFrameHeight: 500,
        initialFrameWidth: '100%',
        UEDITOR_HOME_URL: '/UEditor/',
        serverUrl: '',
      },
      agreement: {
        content: '',
        id: 0,
      },
      spinShow: false,
    };
  },
  created() {
    this.memberAgreement();
  },
  methods: {
    getEditorContent(data) {
      this.agreement.content = data;
    },
    memberAgreement() {
      this.spinShow = true;
      agentAgreement()
        .then((res) => {
          this.spinShow = false;
          const { title, content, status, id } = res.data;
          this.agreement.content = content;
          this.agreement.id = id || 0;
        })
        .catch((err) => {
          this.$Message.error(err.msg);
          this.spinShow = false;
        });
    },
    // 保存
    memberAgreementSave() {
      agentAgreementSave(this.agreement)
        .then((res) => {
          this.$Message.success('保存成功');
          this.memberAgreement();
        })
        .catch((err) => {
          this.$Message.error(err.msg);
        });
    },
  },
};
</script>

<style scoped lang="stylus">
::v-deep .ivu-form-item-content {
  line-height: unset !important;
}
</style>
