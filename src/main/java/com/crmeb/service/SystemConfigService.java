package com.crmeb.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import com.crmeb.service.cache.CacheService;
import java.util.Map;
import java.util.HashMap;
import java.util.List;
import java.util.function.Supplier;

/**
 * System Configuration Service
 * Maps to original SystemConfigService.php functionality
 * Manages system configuration with Redis caching
 *
 * Features:
 * - Single and multiple config retrieval
 * - Redis-based caching
 * - Support for different configuration types
 * - Configurable cache expiration
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class SystemConfigService {

    private static final String CACHE_SYSTEM = "system_config";
    private static final int EXPIRE_TIME = 30 * 24 * 3600; // 30 days

    private final com.crmeb.service.cache.CacheService cacheService;

    /**
     * Get single configuration value
     * @param key configuration key
     * @param defaultValue default value if not found
     * @param useCache whether to use cache
     * @return configuration value
     */
    public Object get(String key, Object defaultValue, boolean useCache) {
        String cacheName = CACHE_SYSTEM + ":" + key;
        
        if (!useCache) {
            return getConfigValue(key, defaultValue);
        }

        return cacheService.get(cacheName, () -> getConfigValue(key, defaultValue), EXPIRE_TIME);
    }

    /**
     * Get multiple configuration values
     * @param keys configuration keys
     * @param useCache whether to use cache
     * @return map of configuration values
     */
    public Map<String, Object> more(List<String> keys, boolean useCache) {
        String cacheName = CACHE_SYSTEM + ":" + String.join(",", keys);
        
        Supplier<Map<String, Object>> configSupplier = () -> {
            Map<String, Object> result = new HashMap<>();
            for (String key : keys) {
                result.put(key, getConfigValue(key, null));
            }
            return result;
        };

        if (!useCache) {
            return configSupplier.get();
        }

        return cacheService.get(cacheName, configSupplier, EXPIRE_TIME);
    }

    /**
     * Clear configuration cache
     * @return true if successful
     */
    public boolean clear() {
        try {
            return cacheService.clear(CACHE_SYSTEM);
        } catch (Exception e) {
            log.error("Failed to clear system config cache", e);
            return false;
        }
    }

    /**
     * Get configuration value from database
     * @param key configuration key
     * @param defaultValue default value if not found
     * @return configuration value
     */
    private Object getConfigValue(String key, Object defaultValue) {
        try {
            // TODO: Implement database lookup using JPA repository
            // For now, return default value
            return defaultValue;
        } catch (Exception e) {
            log.error("Failed to get config value for key: {}", key, e);
            return defaultValue;
        }
    }
}
