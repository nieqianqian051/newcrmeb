package com.crmeb.controller.api;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.http.MediaType;
import com.crmeb.config.SecurityConfig;
import com.crmeb.config.WebMvcConfig;
import com.crmeb.service.SystemConfigService;
import com.crmeb.service.cache.CacheService;
import com.crmeb.service.product.ProductService;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;

/**
 * Product Controller Tests
 * Verifies that product-related endpoints return correct JSON structures
 * matching the original PHP implementation
 *
 * Original routes tested:
 * - GET /api/products (商品列表)
 * - GET /api/product/detail/:id (商品详情)
 * - GET /api/product/hot (热门商品)
 * - GET /api/product/recommend (推荐商品)
 *
 * @author Devin
 * @since 2024-01-xx
 */
@WebMvcTest(ProductController.class)
@AutoConfigureMockMvc
@Import({SecurityConfig.class, WebMvcConfig.class})
public class ProductControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private SystemConfigService systemConfigService;

    @MockBean
    private CacheService cacheService;

    @MockBean
    private ProductService productService;

    @Test
    public void testGetProducts() throws Exception {
        mockMvc.perform(get("/api/products")
                .param("page", "1")
                .param("limit", "10"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code").value(200))
            .andExpect(jsonPath("$.message").value("success"))
            .andExpect(jsonPath("$.data.list").exists())
            .andExpect(jsonPath("$.data.total").exists())
            .andExpect(jsonPath("$.data.page").exists());
    }

    @Test
    public void testGetProductDetail() throws Exception {
        int productId = 1; // Test product ID
        mockMvc.perform(get("/api/product/detail/" + productId))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code").value(200))
            .andExpect(jsonPath("$.message").value("success"))
            .andExpect(jsonPath("$.data.id").exists())
            .andExpect(jsonPath("$.data.name").exists())
            .andExpect(jsonPath("$.data.price").exists())
            .andExpect(jsonPath("$.data.description").exists());
    }

    @Test
    public void testGetHotProducts() throws Exception {
        mockMvc.perform(get("/api/product/hot"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code").value(200))
            .andExpect(jsonPath("$.message").value("success"))
            .andExpect(jsonPath("$.data").isArray());
    }

    @Test
    public void testGetRecommendedProducts() throws Exception {
        mockMvc.perform(get("/api/product/recommend"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code").value(200))
            .andExpect(jsonPath("$.message").value("success"))
            .andExpect(jsonPath("$.data").isArray());
    }
}
