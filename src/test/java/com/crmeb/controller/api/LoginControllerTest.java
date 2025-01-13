package com.crmeb.controller.api;

import com.crmeb.common.ApiResult;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.test.web.servlet.MockMvc;
import com.crmeb.config.SecurityConfig;
import com.crmeb.config.WebMvcConfig;
import com.crmeb.service.SystemConfigService;
import com.crmeb.service.cache.CacheService;
import org.springframework.test.web.servlet.MvcResult;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.mockito.Mockito.when;
import static org.mockito.ArgumentMatchers.any;

/**
 * Login Controller Tests
 * Verifies that login-related endpoints return correct JSON structures
 * matching the original PHP implementation
 *
 * @author Devin
 * @since 2024-01-xx
 */
@WebMvcTest(LoginController.class)
@AutoConfigureMockMvc
@Import({SecurityConfig.class, WebMvcConfig.class})
public class LoginControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private SystemConfigService systemConfigService;

    @MockBean
    private CacheService cacheService;

    @Test
    public void testGetAjCaptcha() throws Exception {
        when(systemConfigService.get("captcha_enabled", true, true)).thenReturn(true);
        when(cacheService.get(any(), any(), any())).thenReturn(null);
        
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
        when(systemConfigService.get("site_logo", "", true)).thenReturn("/admin/images/logo.png");
        when(systemConfigService.get("site_name", "CRMEB PRO 3.1", true)).thenReturn("CRMEB PRO 3.1");
        when(cacheService.get(any(), any(), any())).thenReturn(null);
        
        mockMvc.perform(get("/api/login/info"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code").value(200))
            .andExpect(jsonPath("$.message").value("success"))
            .andExpect(jsonPath("$.data.logo").value("/admin/images/logo.png"))
            .andExpect(jsonPath("$.data.version").value("PRO_V3.1"))
            .andExpect(jsonPath("$.data.name").value("CRMEB PRO 3.1"));
    }
}
