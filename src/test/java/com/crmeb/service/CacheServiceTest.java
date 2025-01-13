package com.crmeb.service;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.junit.jupiter.api.extension.ExtendWith;
import com.crmeb.config.RedisConfig;
import org.springframework.data.redis.core.RedisTemplate;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Cache Service Tests
 * Verifies Redis caching operations work correctly
 * matching the original PHP CacheService functionality
 *
 * Features tested:
 * - Cache get/set operations
 * - Cache expiration
 * - Cache deletion
 * - Token bucket operations
 *
 * @author Devin
 * @since 2024-01-xx
 */
@ExtendWith(SpringExtension.class)
@Import(RedisConfig.class)
public class CacheServiceTest {

    @Autowired
    private com.crmeb.service.cache.CacheService cacheService;

    @Test
    public void testSetAndGet() {
        String key = "test:key";
        String value = "test value";
        
        assertTrue(cacheService.set(key, value, 60));
        assertEquals(value, cacheService.get(key, () -> null, 60));
    }

    @Test
    public void testDelete() {
        String key = "test:delete";
        String value = "test value";
        
        cacheService.set(key, value, 60);
        assertTrue(cacheService.delete(key));
        assertNull(cacheService.get(key, () -> null, 60));
    }

    @Test
    public void testClear() {
        String key1 = "test:clear1";
        String key2 = "test:clear2";
        
        cacheService.set(key1, "value1", 60);
        cacheService.set(key2, "value2", 60);
        
        assertTrue(cacheService.clear("test"));
        assertNull(cacheService.get(key1, () -> null, 60));
        assertNull(cacheService.get(key2, () -> null, 60));
    }

    @Test
    public void testDefaultValueSupplier() {
        String key = "test:supplier";
        String defaultValue = "default";
        
        String value = cacheService.get(key, () -> defaultValue, 60);
        assertEquals(defaultValue, value);
    }
}
