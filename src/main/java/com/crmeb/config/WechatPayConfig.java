package com.crmeb.config;

import com.wechat.pay.java.core.Config;
import com.wechat.pay.java.core.RSAAutoCertificateConfig;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * WeChat Pay Configuration
 * Configures WeChat Pay SDK with merchant credentials
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Configuration
public class WechatPayConfig {

    @Value("${wechat.pay.mchId}")
    private String mchId;

    @Value("${wechat.pay.mchSerialNumber}")
    private String mchSerialNumber;

    @Value("${wechat.pay.privateKey}")
    private String privateKey;

    @Value("${wechat.pay.apiV3Key}")
    private String apiV3Key;

    @Value("${wechat.pay.appId}")
    private String appId;

    @Bean
    public Config createWechatPayConfig() {
        return new RSAAutoCertificateConfig.Builder()
                .merchantId(mchId)
                .privateKeyFromPath(privateKey)
                .merchantSerialNumber(mchSerialNumber)
                .apiV3Key(apiV3Key)
                .build();
    }
}
