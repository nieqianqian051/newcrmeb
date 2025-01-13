package com.crmeb.repository.system;

import com.crmeb.model.system.SystemRole;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repository interface for SystemRole entity
 * Provides database operations for role management
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Repository
public interface SystemRoleRepository extends JpaRepository<SystemRole, Integer> {
    
    /**
     * Find all active roles
     * @return List of active roles
     */
    List<SystemRole> findByStatusTrueAndIsDelFalse();
    
    /**
     * Find role by name
     * @param roleName the role name
     * @return List of roles
     */
    List<SystemRole> findByRoleNameAndStatusTrue(String roleName);
}
