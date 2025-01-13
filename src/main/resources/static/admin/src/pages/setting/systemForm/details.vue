<template>
  <div>
    <div class="i-layout-page-header">
      <PageHeader class="product_tabs" hidden-breadcrumb>
        <div slot="title" class="acea-row row-middle">
          <router-link :to="{ path: `/admin/setting/system_form` }">
            <div class="font-sm after-line">
              <span class="iconfont iconfanhui"></span>
              <span class="pl10">返回</span>
            </div>
          </router-link>
          <span v-text="$route.meta.title" class="mr20 ml16"></span>
        </div>
      </PageHeader>
    </div>
    <Card :bordered="false" dis-hover class="ivu-mt">
      <Row type="flex">
        <Col v-bind="grid">
          <!-- 查询条件 -->
          <Form
            ref="formValidate"
            :model="formValidate"
            :label-width="labelWidth"
            :label-position="labelPosition"
            @submit.native.prevent
          >
            <FormItem label="时间筛选：">
              <DatePicker
                :editable="false"
                :clearable="true"
                @on-change="onchangeTime"
                :value="timeVal"
                format="yyyy/MM/dd"
                type="datetimerange"
                placement="bottom-start"
                placeholder="自定义时间"
                class="input-add"
                :options="options"
              ></DatePicker>
            </FormItem>
          </Form>
          <Button type="primary" @click="systemFormExport">导出</Button>
        </Col>
      </Row>
    </Card>
    <Card :bordered="false" dis-hover class="ivu-mt">
      <Table :columns="columns" :data="tableData">
        <template slot-scope="{ row, index }" slot="content">
          <div v-for="(item,i) in row.content" :key="i">
            <div v-if="item.type != 'uploadPicture'" class="mb-10">{{item.title}}:{{item.value}}</div>
            <div v-else class="acea-row row-middle">
              <span>{{item.title}}:</span>
              <img class="block ml-14 w-100" v-for="(pic,j) in item.value" :src="pic" v-viewer />
            </div>
          </div>
        </template>
      </Table>
      <div class="acea-row row-right page">
        <Page
          :total="total"
          show-elevator
          show-total
          @on-change="pageChange"
          :page-size="formValidate.limit"
        />
      </div>
    </Card>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import { systemFormData, systemFormDataExport } from '@/api/system';
import timeOptions from '@/utils/timeOptions';
import exportExcel from '@/utils/newToExcel.js';
import Setting from '@/setting'
export default {
  data() {
    return {
      grid: {
        xl: 7,
        lg: 7,
        md: 12,
        sm: 24,
        xs: 24,
      },
      formValidate: {
        data: 'thirtyday',
        page: 1,
        limit: 20,
      },
      columns: [
        {
          title: '模板名称',
          key: 'system_form_name',
          width: 130,
        },
        {
          title: '用户名称/ID',
          key: 'nickname',
          width: 130,
          render: (h, params) => {
            return h('div', `${params.row.nickname}/${params.row.uid}`);
          },
        },
        {
          title: '用户手机号',
          key: 'phone',
          width: 130,
        },
        {
          title: '模板内容',
          slot: 'content',
          tooltip: true,
          minWidth: 80,
        },
        {
          title: '创建时间',
          key: 'add_time',
          width: 130,
        },
      ],
      tableData: [],
      total: 0,
      timeVal: [],
      options: timeOptions,
    };
  },
  computed: {
    ...mapState('admin/layout', ['isMobile']),
    labelWidth() {
      return this.isMobile ? undefined : 80;
    },
    labelPosition() {
      return this.isMobile ? 'top' : 'right';
    },
  },
  created() {
    this.systemFormData();
  },
  methods: {
    // 具体日期
    onchangeTime(e) {
      this.timeVal = e;
      this.formValidate.data = this.timeVal[0] ? this.timeVal.join('-') : '';
      if (e[0] == '') {
        this.formValidate.data = 'thirtyday';
      }
      this.formValidate.page = 1;
      this.systemFormData();
    },
    systemFormData() {
      systemFormData(this.$route.query.id, this.formValidate).then((res) => {
        res.data.list.map(item=>{
          this.$set(item,'content',item.value);
        })
        this.tableData = res.data.list;
        this.total = res.data.count;
      });
    },
    systemFormDataExport(formValidate) {
      return new Promise((resolve) => {
        systemFormDataExport(this.$route.query.id, formValidate).then((res) => {
          resolve(res.data);
        });
      });
    },
    async systemFormExport() {
      let formValidate = { ...this.formValidate, page: 1 };
      let headers = [];
      let filenames = '';
      let filekeys = [];
      let sheetData = [];
      for (let i = 0; i < formValidate.page; i++) {
        let result = await this.systemFormDataExport(formValidate);
        let { header, filename, filekey } = result;
        if (!result.export.length) {
          break;
        }
        if (header.length) {
          headers = header;
        }
        if (filename) {
          filenames = filename;
        }
        if (filekey.length) {
          filekeys = filekey;
        }
        sheetData = sheetData.concat(result.export);
        formValidate.page++;
      }
      for (const row of sheetData) {
        row.content = '';
        for (const item of row.form_data) {
          row.content += `${item.title}：${item.value}；`;
        }
        row.form_data = row.content;
      }
      exportExcel(headers, filekeys, filenames, sheetData);
    },
    pageChange(index) {
      this.formValidate.page = index;
      this.systemFormData();
      let arr = []; arr.includes()
    },
  },
};
</script>

<style>
.map{
  background-repeat: no-repeat;
}
</style>
