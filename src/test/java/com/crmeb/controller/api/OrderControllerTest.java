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
 * Order Controller Tests
 * Verifies that order-related endpoints return correct JSON structures
 * matching the original PHP implementation
 *
 * Original routes tested:
 * - GET /api/order/list (订单列表)
 * - GET /api/order/detail/:uni (订单详情)
 * - POST /api/order/create/:key (创建订单)
 * - POST /api/order/pay (订单支付)
 * - POST /api/order/cancel (取消订单)
 *
 * @author Devin
 * @since 2024-01-xx
 */
@SpringBootTest
@AutoConfigureMockMvc
public class OrderControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    public void testGetOrderList() throws Exception {
        mockMvc.perform(get("/api/order/list")
                .param("page", "1")
                .param("limit", "10")
                .param("status", "0"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code").value(200))
            .andExpect(jsonPath("$.message").value("success"))
            .andExpect(jsonPath("$.data.list").exists())
            .andExpect(jsonPath("$.data.total").exists())
            .andExpect(jsonPath("$.data.page").exists());
    }

    @Test
    public void testGetOrderDetail() throws Exception {
        String orderUni = "TEST123456"; // Test order number
        mockMvc.perform(get("/api/order/detail/" + orderUni))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code").value(200))
            .andExpect(jsonPath("$.message").value("success"))
            .andExpect(jsonPath("$.data.order_id").exists())
            .andExpect(jsonPath("$.data.total_price").exists())
            .andExpect(jsonPath("$.data.paid").exists())
            .andExpect(jsonPath("$.data.status").exists());
    }

    @Test
    public void testCreateOrder() throws Exception {
        String key = "TEST_KEY"; // Test cart key
        String orderJson = "{\"address_id\":1,\"pay_type\":\"weixin\",\"use_integral\":0}";
        
        mockMvc.perform(post("/api/order/create/" + key)
                .contentType(MediaType.APPLICATION_JSON)
                .content(orderJson))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code").value(200))
            .andExpect(jsonPath("$.message").value("success"))
            .andExpect(jsonPath("$.data.order_id").exists());
    }

    @Test
    public void testPayOrder() throws Exception {
        String payJson = "{\"uni\":\"TEST123456\",\"paytype\":\"weixin\",\"from\":\"wechat\"}";
        
        mockMvc.perform(post("/api/order/pay")
                .contentType(MediaType.APPLICATION_JSON)
                .content(payJson))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code").value(200))
            .andExpect(jsonPath("$.message").value("success"));
    }

    @Test
    public void testCancelOrder() throws Exception {
        String cancelJson = "{\"uni\":\"TEST123456\"}";
        
        mockMvc.perform(post("/api/order/cancel")
                .contentType(MediaType.APPLICATION_JSON)
                .content(cancelJson))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code").value(200))
            .andExpect(jsonPath("$.message").value("success"));
    }
}
