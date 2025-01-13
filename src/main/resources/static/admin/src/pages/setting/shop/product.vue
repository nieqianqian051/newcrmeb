<template>
<!-- 商品设置 -->
    <from-submit :validate="ruleValidate" :url="url" :title="title" :rules="rules"/>
</template>

<script>
    import fromSubmit from '@/components/fromSubmit/fromSubmit.vue';
    import buildData from "./buildData";

    export default {
        name: "product",
        components:{fromSubmit},
        mixins:[buildData],
        data() {
            return {
                ruleValidate: {},
                rules: [],
                url: '',
                title:'商品设置',
                type: 'product'
            };
        },
    }
</script>

<style scoped>

</style>
