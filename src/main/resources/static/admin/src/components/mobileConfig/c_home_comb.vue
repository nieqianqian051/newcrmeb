<template>
    <div class="mobile-config">
        <div  v-for="(item,key) in rCom" :key="key">
            <component :is="item.components.name" :configObj="configObj" ref="childData" :configNme="item.configNme" :key="key" :index="activeIndex" :num="item.num"></component>
        </div>
        <rightBtn :activeIndex="activeIndex" :configObj="configObj"></rightBtn>
    </div>
</template>

<script>
import toolCom from '@/components/mobileConfigRight/index.js';
import rightBtn from '@/components/rightBtn/index.vue';
import { mapState, mapMutations, mapActions } from 'vuex';
export default {
  name: 'c_home_comb',
  componentsName: 'home_comb',
  components: {
    ...toolCom,
    rightBtn
  },
  props: {
    activeIndex: {
      type: null
    },
    num: {
      type: null
    },
    index: {
      type: null
    }
  },
  data() {
    return {
      configObj: {},
      rCom: [
        {
          components: toolCom.c_set_up,
          configNme: 'setUp'
        }
      ],
	  oneStyle: [
		{
			components: toolCom.c_title,
			configNme: 'titleRight'
		},
		{
		    components: toolCom.c_slider,
		    configNme: 'contentConfig'
		},
		{
		  components: toolCom.c_bg_color,
		  configNme: 'classColor'
		},
		{
			components: toolCom.c_title,
			configNme: 'titlePointer'
		},
		{
		    components: toolCom.c_radio,
		    configNme: 'docConfig'
		},
		{
		    components: toolCom.c_radio,
		    configNme: 'docPosition'
		},
		{
		    components: toolCom.c_radio,
		    configNme: 'toneConfig'
		}
	  ],
	  twoStyle:[
	  	{
	  	    components: toolCom.c_bg_color,
	  	    configNme: 'dotColor'
	  	},
	  	{
	  	    components: toolCom.c_bg_color,
	  	    configNme: 'dotBgColor'
	  	}
	  ],
	  threeStyle:[
	  	{
	  		components: toolCom.c_title,
	  		configNme: 'titleImg'
	  	},
	  	{
	  	    components: toolCom.c_fillet,
	  	    configNme: 'filletImg'
	  	}
	  ],
	  setUp:0,
	  type:0
    };
  },
  watch: {
    num(nVal) {
      const value = JSON.parse(JSON.stringify(this.$store.state.admin.mobildConfig.defaultArray[nVal]));
      this.configObj = value;
    },
    configObj: {
      handler(nVal, oVal) {
        this.$store.commit('admin/mobildConfig/UPDATEARR', { num: this.num, val: nVal });
      },
      deep: true
    },
    'configObj.setUp.tabVal': {
      handler(nVal, oVal) {
		this.setUp = nVal;
        var arr = [this.rCom[0]];
        if (nVal == 0) {
          const tempArr = [
			{
				components: toolCom.c_title,
				configNme: 'titleLeft'
			},
			{
			    components: toolCom.c_radio,
			    configNme: 'styleConfig'
			},
			{
			    components: toolCom.c_radio,
			    configNme: 'classConfig'
			},
			{
			    components: toolCom.c_radio,
			    configNme: 'searchConfig'
			},
			{
				components: toolCom.c_title,
				configNme: 'titleSearch'
			},
            {
              components: toolCom.c_upload_img,
              configNme: 'logoConfig'
            },
			{
			  components: toolCom.c_input_item,
			  configNme: 'inputConfig'
			},
			{
				components: toolCom.c_title,
				configNme: 'titleHotWords'
			},
			{
			  components: toolCom.c_hot_word,
			  configNme: 'hotWords'
			},
            {
              components: toolCom.c_input_number,
              configNme: 'numConfig'
            },
			{
			  components: toolCom.c_title,
			  configNme: 'titleTab'
			},
			{
			  components: toolCom.c_tab_list,
			  configNme: 'tabListConfig'
			},
			{
			  components: toolCom.c_title,
			  configNme: 'titleImg'
			},
			{
			  components: toolCom.c_menu_list,
			  configNme: 'swiperConfig'
			}
          ];
          this.rCom = arr.concat(tempArr);
        } else {
		   if(this.type){
			   this.rCom = [...arr,...this.oneStyle,...this.twoStyle,...this.threeStyle]
		   }else{
			   this.rCom = [...arr,...this.oneStyle,...this.threeStyle]
		   }
        }
      },
      deep: true
    },
	'configObj.toneConfig.tabVal':{
		handler(nVal, oVal) {
		  this.type = nVal;
		  var arr = [this.rCom[0]];
		  if(this.setUp){
			if(nVal){
				this.rCom = [...arr,...this.oneStyle,...this.twoStyle,...this.threeStyle]
			}else{
				this.rCom = [...arr,...this.oneStyle,...this.threeStyle]
			}
		  }
		}
	}
  },
  mounted() {
    this.$nextTick(() => {
      const value = JSON.parse(JSON.stringify(this.$store.state.admin.mobildConfig.defaultArray[this.num]));
      this.configObj = value;
    });
  },
  methods: {
    handleSubmit(name) {
      const obj = {};
      obj.activeIndex = this.activeIndex;
      obj.data = this.configObj;
      this.add(obj);
    },
    ...mapMutations({
      add: 'admin/mobildConfig/UPDATEARR'
    })
  }
};
</script>

<style scoped lang="stylus">
    .title-tips
        padding-bottom 10px
        font-size 14px
        color #333
        span
            margin-right 14px
            color #999
</style>
