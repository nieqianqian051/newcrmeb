package com.crmeb.service;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.redis.core.RedisTemplate;

import java.util.Arrays;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

/**
 * System Configuration Service Tests
 * Verifies configuration management and caching functionality
 * matching the original PHP SystemConfigService implementation
 *
 * Features tested:
 * - Single config retrieval
 * - Multiple config retrieval
 * - Cache management
 * - Default value handling
 *
 * @author Devin
 * @since 2024-01-xx
 */
@SpringBootTest
public class SystemConfigServiceTest {

    @Autowired
    private SystemConfigService systemConfigService;

    @MockBean
    private CacheService cacheService;

    @Test
    public void testGetSingleConfig() {
        String key = "site_name";
        String value = "CRMEB PRO";
        
        when(cacheService.get(any(), any(), any())).thenReturn(value);
        
        Object result = systemConfigService.get(key, "", true);
        assertEquals(value, result);
    }

    @Test
    public void testGetMultipleConfigs() {
        when(cacheService.get(any(), any(), any())).thenReturn(Map.of(
            "site_name", "CRMEB PRO",
            "site_url", "http://localhost",
            "site_logo", "/logo.png"
        ));
        
        Map<String, Object> result = systemConfigService.more(Arrays.asList(
            "site_name",
            "site_url",
            "site_logo"
        ), true);
        
        assertNotNull(result);
        assertEquals(3, result.size());
        assertEquals("CRMEB PRO", result.get("site_name"));
        assertEquals("http://localhost", result.get("site_url"));
        assertEquals("/logo.png", result.get("site_logo"));
    }

    @Test
    public void testClearCache() {
        when(cacheService.clear(any())).thenReturn(true);
        assertTrue(systemConfigService.clear());
    }

    @Test
    public void testGetDefaultValue() {
        String key = "non_existent_key";
        String defaultValue = "default";
        
        when(cacheService.get(any(), any(), any())).thenReturn(null);
        
        Object result = systemConfigService.get(key, defaultValue, true);
        assertEquals(defaultValue, result);
    }
}
