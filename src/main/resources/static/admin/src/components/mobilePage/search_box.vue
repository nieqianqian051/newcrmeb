<template>
	<div :style="{
		background:bottomBgColor,
		paddingTop:topConfig+'px',
		paddingBottom:bottomConfig+'px',
		paddingLeft:prConfig+'px',
		paddingRight:prConfig+'px'
	}">
		<div class="search-box" :style="{
			background: `linear-gradient(90deg,${bgColorLeft} 0%,${bgColorRight} 100%)`,
			borderRadius:bgRadius
			}">
			<div class="search" v-if="styleConfig == 2">
				<div class="box acea-row row-between-wrapper" v-if="styleSearchConfig == 1" :style="{
					background:searchBoxColor
				}">
				  <div>
					 <span class="iconfont iconsousuo1" :style="{
					 	color:tipColor
					 }"></span>
					 <span class="hotWords" :style="{
					 	color:hotWordsColor
					 }" v-if="hotWords">{{hotWords}}</span>
					 <span v-else :style="{
					 	color:tipColor
					 }">{{tipConfig}}</span>
				  </div>
				  <div class="text" :style="{
					background:toneConfig?searchBgColor:colorStyle.theme,
					color: toneConfig?searchTxtColor:'#fff'
				  }">搜索</div>
				</div>
				<div class="acea-row row-center-wrapper" v-else>
					<div class="box" :class="styleSearchConfig == 0?'on':''" :style="{
						background:searchBoxColor
					}">
						<span class="iconfont iconsousuo1" :style="{
							color:tipColor
						}"></span>
						<span class="hotWords" :style="{
							color:hotWordsColor
						}" v-if="hotWords">{{hotWords}}</span>
						<span v-else :style="{
							color:tipColor
						}">{{tipConfig}}</span>
					</div>
					<span class="text2" v-if="styleSearchConfig == 2" :style="{
						color:toneConfig?searchColor:colorStyle.theme
					}">搜索</span>
				</div>
			</div>
			<div class="search acea-row row-center-wrapper" v-else>
				<img :src="logoUrl" alt="" v-if="logoUrl && styleConfig == 0">
				<div class="title" v-if="titleConfig && styleConfig == 1">{{titleConfig}}</div>
				<div class="box" :style="{
					background:searchBoxColor
				}">
					<span class="iconfont iconsousuo1" :style="{
						color:tipColor
					}"></span>
					<span class="hotWords" :style="{
						color:hotWordsColor
					}" v-if="hotWords">{{hotWords}}</span>
					<span v-else :style="{
						color:tipColor
					}">{{tipConfig}}</span>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
    import { mapState } from 'vuex'
	// import theme from "@/mixins/theme";
    export default {
        name: 'search_box',
        cname: '搜索框',
        icon: '#iconzujian-sousuokuang',
        configName: 'c_search_box',
        type:0,// 0 基础组件 1 营销组件 2工具组件
        defaultName:'headerSerch', // 外面匹配名称
        props: {
            index: {
                type: null
            },
            num: {
                type: null
            },
			colorStyle:{
				type: null
			}
        },
        computed: {
            ...mapState('admin/mobildConfig', ['defaultArray'])
        },
        watch: {
            pageData: {
                handler (nVal, oVal) {
                    this.setConfig(nVal)
                },
                deep: true
            },
            num: {
                handler (nVal, oVal) {
                    let data = this.$store.state.admin.mobildConfig.defaultArray[nVal]
                    this.setConfig(data)
                },
                deep: true
            },
            'defaultArray': {
                handler (nVal, oVal) {
                    let data = this.$store.state.admin.mobildConfig.defaultArray[this.num]
                    this.setConfig(data);
                },
                deep: true
            }
        },
        // mixins: [theme],
		data () {
            return {
                // 默认初始化数据禁止修改
                defaultConfig: {
					cname: '搜索框',
                    name: 'headerSerch',
                    timestamp: this.num,
					isHide:false,
                    setUp: {
                        tabVal: 0
                    },
					titleLeft:'展示设置',
					titleSearch:'搜索内容',
					titleHotWords:'搜索热词',
					titleRight:'搜索框',
					titleCurrency:'通用样式',
					styleConfig:{
						title: '选择风格',
						tabVal: 0,
						tabList: [
							{
							  name: 'logo+搜索'
							},
						    {
						      name: '标题+搜索'
						    },
							{
							  name: '搜索'
							}
						]
					},
					logoConfig:{
						info: '建议：144px * 44px',
						url: '',
						type:'code',
						delType:1,
						name:'logo图'
					},
					titleConfig:{
						title: '标题',
						value: '标题',
						place: '请输入标题',
						max: 6
					},
					styleSearchConfig:{
						title: '选择风格',
						tabVal: 0,
						tabList: [
							{
							  name: '样式1'
							},
						    {
						      name: '样式2'
						    },
							{
							  name: '样式3'
							}
						]
					},
					tipConfig:{
						title: '提示文字',
						value: '搜索商品',
						place: '填写内容',
						max: 20
					},
					hotWords: {
					  list: [
					    {
					      val: ''
					    }
					  ]
					},
					numConfig: {
					  placeholder: '设置搜索热词显示时间',
					  title: '显示时间',
					  val: 3,
					  type:'words'
					},
					searchBoxColor:{
						title: '搜索框',
						default: [
						    {
						        item: '#F5F5F5'
						    }
						],
						color: [
						    {
						        item: '#F5F5F5'
						    }
						]
					},
					tipColor:{
						title: '提示文字',
						default: [
						    {
						        item: '#CCCCCC'
						    }
						],
						color: [
						    {
						        item: '#CCCCCC'
						    }
						]
					},
					hotWordsColor:{
						title: '热词文字',
						default: [
						    {
						        item: '#888'
						    }
						],
						color: [
						    {
						        item: '#888'
						    }
						]
					},
					toneConfig:{
						title: '色调',
						tabVal: 0,
						tabList: [
							{
							  name: '跟随主题风格'
							},
						    {
						      name: '自定义'
						    }
						]
					},
					searchColor:{
						title: '搜索文字',
						default: [
						    {
						        item: '#E93323'
						    }
						],
						color: [
						    {
						        item: '#E93323'
						    }
						]
					},
					searchTxtColor:{
						title: '搜索文字',
						default: [
						    {
						        item: '#fff'
						    }
						],
						color: [
						    {
						        item: '#fff'
						    }
						]
					},
					searchBgColor:{
						title: '搜索背景',
						default: [
						    {
						        item: '#E93323'
						    }
						],
						color: [
						    {
						        item: '#E93323'
						    }
						]
					},
					moduleColor:{
						title: '组件背景',
						default: [
						    {
						        item: '#fff'
						    },
							{
							    item: '#fff'
							}
						],
						color: [
						    {
						        item: '#fff'
						    },
							{
							    item: '#fff'
							}
						]
					},
					bottomBgColor:{
						title: '底部背景',
						default: [
						    {
						        item: '#fff'
						    }
						],
						color: [
						    {
						        item: '#fff'
						    }
						]
					},
					topConfig: {
						title: '上边距',
						val: 0,
						min: 0
					},
					bottomConfig: {
						title: '下边距',
						val: 0,
						min: 0
					},
					prConfig: {
					    title: '左右边距',
					    val: 0,
					    min: 0
					},
					fillet:{
						title:'背景圆角',
						type: 0,
						list: [
						  {
						    val: "全部",
						    icon: "iconcaozuo-zhengti",
						  },
						  {
						    val: "单个",
						    icon: "iconcaozuo-bianjiao",
						  }
						],
						valName:'圆角值',
						val: 0,
						min: 0,
						valList:[
							{val:0},
							{val:0},
							{val:0},
							{val:0}
						]
					}    
                },
                pageData: {},
                logoUrl:'',
				styleConfig:0,
				bottomBgColor:'',
				bgColorLeft:'',
				bgColorRight:'',
				topConfig:0,
				bottomConfig:0,
				prConfig:0,
				bgRadius:0,
				titleConfig:'',
				searchBoxColor:'',
				styleSearchConfig:0,
				searchColor:'',
				searchBgColor:'',
				tipConfig:'',
				hotWords:'',
				tipColor:'',
				hotWordsColor:'',
				searchTxtColor:''
            }
        },
        mounted () {
            this.$nextTick(() => {
                this.pageData = this.$store.state.admin.mobildConfig.defaultArray[this.num]
                this.setConfig(this.pageData)
            })
        },
        methods: {
            setConfig (data) {
                if(!data) return
                if(data.prConfig){
                    this.logoUrl = data.logoConfig.url;
					this.styleConfig = data.styleConfig.tabVal;
					this.bottomBgColor = data.bottomBgColor.color[0].item;
					this.bgColorLeft = data.moduleColor.color[0].item;
					this.bgColorRight = data.moduleColor.color[1].item;
					this.topConfig = data.topConfig.val;
					this.bottomConfig = data.bottomConfig.val;
					this.prConfig = data.prConfig.val;
					this.titleConfig = data.titleConfig.value;
					this.searchBoxColor = data.searchBoxColor.color[0].item;
					this.styleSearchConfig = data.styleSearchConfig.tabVal;
					this.searchColor = data.searchColor.color[0].item;
					this.toneConfig = data.toneConfig.tabVal;
					this.searchBgColor = data.searchBgColor.color[0].item;
					this.tipConfig = data.tipConfig.value;
					this.hotWords = data.hotWords.list.length?data.hotWords.list[0].val:'';
					this.tipColor = data.tipColor.color[0].item;
					this.hotWordsColor = data.hotWordsColor.color[0].item;
					this.searchTxtColor = data.searchTxtColor.color[0].item;
					let fillet = data.fillet.type;
					let filletVal = data.fillet.val
					let valList = data.fillet.valList;
					this.bgRadius = fillet? valList[0].val+ 'px ' +valList[1].val + 'px ' + valList[3].val + 'px ' + valList[2].val +'px' : filletVal +'px';
                }
            }
        }
    }
</script>

<style scoped lang="stylus">
.search-box{
	display: flex
	align-items: center
	justify-content: center
	width: 100%
	height: 48px
	padding: 9px 15px
	cursor: pointer;
	.search{
		width: 100%
		.text{
			width: 46px;
			height: 26px;
			border-radius: 13px;
			text-align: center;
			line-height: 26px;
			color: #fff;
			font-size: 11px;
		}
		.text2{
			font-size: 15px;
			margin-left: 10px;
		}
		.hotWords{
			color: rgba(255,255,255,0.8);
		}
	}
	.title{
	    margin-right: 15px;
	    font-size: 15px;
		color: #333;
	}
	.map{
	    color: #fff;
	    font-size: 15px
	    margin-right: 11px
	    .iconfont{
	        font-size: 16px;
	    }
	    .iconxiayi{
	        font-size: 12px;
	    }
	}
	img{
		width: 76px
		height: 30px
		margin-right: 11px
	}
	.box{
		flex: 1
		height: 30px
		line-height: 30px
		color: #ccc
		font-size: 14px
		padding-left: 16px
		background: #fff
		border-radius:15px;
		
		&.on{
			text-align: center
		}
		.iconfont{
		    margin-right: 5px
		    margin-top: -3px;
		    display: inline-block;
		    vertical-align: middle;
		}
	}
}
</style>
