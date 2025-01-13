package com.crmeb.controller.api;

import com.crmeb.common.ApiResult;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;

/**
 * Login Controller Tests
 * Verifies that login-related endpoints return correct JSON structures
 * matching the original PHP implementation
 *
 * @author Devin
 * @since 2024-01-xx
 */
@SpringBootTest
@AutoConfigureMockMvc
public class LoginControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    public void testGetAjCaptcha() throws Exception {
        mockMvc.perform(get("/api/ajcaptcha"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code").value(200))
            .andExpect(jsonPath("$.message").value("success"))
            .andExpect(jsonPath("$.data.captchaType").value("blockPuzzle"))
            .andExpect(jsonPath("$.data.projectCode").value("crmeb"))
            .andExpect(jsonPath("$.data.captchaOriginalPath").value("/api/captcha/original"))
            .andExpect(jsonPath("$.data.captchaVerifyPath").value("/api/captcha/verify"));
    }

    @Test
    public void testGetLoginInfo() throws Exception {
        mockMvc.perform(get("/api/login/info"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code").value(200))
            .andExpect(jsonPath("$.message").value("success"))
            .andExpect(jsonPath("$.data.logo").value("/admin/images/logo.png"))
            .andExpect(jsonPath("$.data.version").value("PRO_V3.1"))
            .andExpect(jsonPath("$.data.name").value("CRMEB PRO 3.1"));
    }
}
