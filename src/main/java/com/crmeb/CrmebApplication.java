package com.crmeb;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.transaction.annotation.EnableTransactionManagement;

@SpringBootApplication(scanBasePackages = {
    "com.crmeb.controller",
    "com.crmeb.config",
    "com.crmeb.service",
    "com.crmeb.security",
    "com.crmeb.websocket"
})
@EnableScheduling
@EnableTransactionManagement
public class CrmebApplication {
    public static void main(String[] args) {
        SpringApplication.run(CrmebApplication.class, args);
    }
}
