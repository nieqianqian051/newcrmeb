<template>
    <!-- 事业部设置 -->
        <from-submit :validate="ruleValidate" :url="url" :title="title" :rules="rules"/>
    </template>
    
    <script>
        import fromSubmit from '@/components/fromSubmit/fromSubmit.vue';
        import buildData from "./buildData";
    
        export default {
            name: "division",
            components:{fromSubmit},
            mixins:[buildData],
            data() {
                return {
                    ruleValidate: {},
                    rules: [],
                    url: '',
                    title:'事业部设置',
                    type: 'division'
                };
            },
        }
    </script>
    
    <style scoped>
    
    </style>
    