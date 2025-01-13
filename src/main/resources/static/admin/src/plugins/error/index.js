// +----------------------------------------------------------------------
// | CRMEB [ CRMEB赋能开发者，助力企业发展 ]
// +----------------------------------------------------------------------
// | Copyright (c) 2016~2021 https://www.crmeb.com All rights reserved.
// +----------------------------------------------------------------------
// | Licensed CRMEB并不是自由软件，未经许可不能去掉CRMEB相关版权
// +----------------------------------------------------------------------
// | Author: CRMEB Team <admin@crmeb.com>
// +----------------------------------------------------------------------
import store from '@/store';
import util from '@/libs/util';
import axios from 'axios';

export default {
    install (Vue, options) {
        Vue.config.errorHandler = function (error, instance, info) {
            Vue.nextTick(() => {
                // store 追加 log
                store.dispatch('admin/log/push', {
                    message: `${info}: ${error.message}`,
                    type: 'error',
                    meta: {
                        error
                        // instance
                    }
                });
            })
        }
    }
}
