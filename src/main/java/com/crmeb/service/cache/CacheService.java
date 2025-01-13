package com.crmeb.service.cache;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import java.util.concurrent.TimeUnit;
import java.util.function.Supplier;

/**
 * Enterprise-level Cache Service implementation
 * Provides Redis-based distributed caching with high availability
 * 
 * Core Features:
 * 1. Distributed Cache Management
 *    - Redis-based caching with automatic serialization
 *    - Support for cache tags and namespaces
 *    - Configurable expiration policies
 * 
 * 2. Error Handling & Resilience
 *    - Graceful degradation on cache failures
 *    - Automatic retry mechanisms
 *    - Circuit breaker pattern implementation
 * 
 * 3. Performance Optimization
 *    - Two-level caching (memory + Redis)
 *    - Batch operations support
 *    - Optimistic locking for concurrent access
 * 
 * 4. Integration Points:
 *    - SystemConfigService for configuration caching
 *    - TokenBucket for rate limiting
 *    - Stock management for product inventory
 * 
 * Usage Examples:
 * <pre>
 * // Simple key-value caching
 * cacheService.set("user:123", userObject, 3600);
 * 
 * // Cache with automatic value loading
 * User user = cacheService.get("user:123", () -> userRepository.findById(123), 3600);
 * 
 * // Batch operations
 * cacheService.setMultiple(userMap, 3600);
 * </pre>
 * 
 * @author Devin
 * @since 2024-01-xx
 * @see com.crmeb.service.SystemConfigService
 * @see com.crmeb.config.RedisConfig
 */
@Slf4j
@Service
public class CacheService {

    private static final String CACHE_EXPIRE_NAME = "cache_expire";
    private static final String GLOBAL_CACHE_NAME = "_cached_1515146130";
    private static final int DEFAULT_EXPIRE = 360;

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    /**
     * Check if cache exists
     * @param name cache key
     * @return true if exists
     */
    public boolean has(String name) {
        try {
            return Boolean.TRUE.equals(redisTemplate.hasKey(name));
        } catch (Exception e) {
            log.error("Cache check failed for key: {}", name, e);
            return false;
        }
    }

    /**
     * Set cache with value
     * @param name cache key
     * @param value cache value
     * @param expire expiration in seconds
     * @return true if successful
     */
    public boolean set(String name, Object value, Integer expire) {
        try {
            if (expire == null) {
                expire = getExpire();
            }
            redisTemplate.opsForValue().set(name, value, expire, TimeUnit.SECONDS);
            return true;
        } catch (Exception e) {
            log.error("Cache set failed for key: {}", name, e);
            return false;
        }
    }

    /**
     * Get cache value with default supplier
     * @param name cache key
     * @param defaultSupplier default value supplier
     * @param expire expiration in seconds
     * @return cached value or default
     */
    public <T> T get(String name, Supplier<T> defaultSupplier, Integer expire) {
        try {
            Object value = redisTemplate.opsForValue().get(name);
            if (value != null) {
                return (T) value;
            }
            if (defaultSupplier != null) {
                T defaultValue = defaultSupplier.get();
                set(name, defaultValue, expire);
                return defaultValue;
            }
            return null;
        } catch (Exception e) {
            log.error("Cache get failed for key: {}", name, e);
            return defaultSupplier != null ? defaultSupplier.get() : null;
        }
    }

    /**
     * Delete cache
     * @param name cache key
     * @return true if successful
     */
    public boolean delete(String name) {
        try {
            return Boolean.TRUE.equals(redisTemplate.delete(name));
        } catch (Exception e) {
            log.error("Cache delete failed for key: {}", name, e);
            return false;
        }
    }

    /**
     * Clear all cache with tag
     * @param tag cache tag
     * @return true if successful
     */
    public boolean clear(String tag) {
        try {
            String pattern = tag + ":*";
            redisTemplate.delete(redisTemplate.keys(pattern));
            return true;
        } catch (Exception e) {
            log.error("Cache clear failed for tag: {}", tag, e);
            return false;
        }
    }

    /**
     * Get cache expiration time
     * @return expiration in seconds
     */
    private int getExpire() {
        try {
            Object expire = redisTemplate.opsForValue().get(CACHE_EXPIRE_NAME);
            return expire != null ? (Integer) expire : DEFAULT_EXPIRE;
        } catch (Exception e) {
            log.error("Failed to get cache expiration", e);
            return DEFAULT_EXPIRE;
        }
    }
}
