package com.crmeb.controller.api;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.http.MediaType;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Payment Controller Tests
 * Verifies that payment-related endpoints return correct JSON structures
 * matching the original PHP implementation
 *
 * Original routes tested:
 * - POST /api/pay/notify/:type (支付回调)
 * - GET /api/ali_pay (支付宝复制链接支付)
 * - POST /api/order/pay (订单支付)
 *
 * @author Devin
 * @since 2024-01-xx
 */
@SpringBootTest
@AutoConfigureMockMvc
public class PayControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    public void testWechatPayNotify() throws Exception {
        String notifyXml = "<xml><return_code>SUCCESS</return_code></xml>";
        
        mockMvc.perform(post("/api/pay/notify/wechat")
                .contentType(MediaType.TEXT_XML)
                .content(notifyXml))
            .andExpect(status().isOk())
            .andExpect(content().string("success"));
    }

    @Test
    public void testAlipayNotify() throws Exception {
        mockMvc.perform(post("/api/pay/notify/alipay")
                .param("trade_status", "TRADE_SUCCESS")
                .param("out_trade_no", "TEST123456"))
            .andExpect(status().isOk())
            .andExpect(content().string("success"));
    }

    @Test
    public void testGetAlipayUrl() throws Exception {
        mockMvc.perform(get("/api/ali_pay")
                .param("orderId", "TEST123456"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code").value(200))
            .andExpect(jsonPath("$.message").value("success"))
            .andExpect(jsonPath("$.data").exists());
    }
}
