package com.crmeb.repository.system;

import com.crmeb.model.system.SystemConfig;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

/**
 * System Configuration Repository
 * Handles database operations for system configuration
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Repository
public interface SystemConfigRepository extends JpaRepository<SystemConfig, Integer> {
    
    /**
     * Find configuration by menu name
     * @param menuName configuration key
     * @return optional configuration
     */
    Optional<SystemConfig> findByMenuName(String menuName);
}
