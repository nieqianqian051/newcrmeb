package com.crmeb.repository.system;

import com.crmeb.model.system.SystemAdmin;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * Repository interface for SystemAdmin entity
 * Provides database operations for administrator management
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Repository
public interface SystemAdminRepository extends JpaRepository<SystemAdmin, Integer> {
    
    /**
     * Find admin by account
     * @param account admin account
     * @return Optional containing admin if found
     */
    Optional<SystemAdmin> findByAccountAndStatusTrueAndIsDelFalse(String account);
    
    /**
     * Check if account exists
     * @param account admin account
     * @return true if account exists
     */
    boolean existsByAccount(String account);
}
