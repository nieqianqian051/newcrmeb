package com.crmeb.config;

import com.alipay.easysdk.factory.Factory;
import com.alipay.easysdk.kernel.Config;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

import javax.annotation.PostConstruct;

/**
 * Alipay Configuration
 * Configures Alipay SDK with merchant credentials
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Configuration
public class AlipayConfig {

    @Value("${alipay.appId}")
    private String appId;

    @Value("${alipay.privateKey}")
    private String privateKey;

    @Value("${alipay.publicKey}")
    private String publicKey;

    @Value("${alipay.notifyUrl}")
    private String notifyUrl;

    @Value("${alipay.returnUrl}")
    private String returnUrl;

    @PostConstruct
    public void init() {
        Config config = new Config();
        config.protocol = "https";
        config.gatewayHost = "openapi.alipay.com";
        config.signType = "RSA2";
        
        config.appId = appId;
        config.merchantPrivateKey = privateKey;
        config.alipayPublicKey = publicKey;
        config.notifyUrl = notifyUrl;

        Factory.setOptions(config);
    }
}
