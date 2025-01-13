package com.crmeb.repository.system;

import com.crmeb.model.system.SystemMenu;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repository interface for SystemMenu entity
 * Provides database operations for menu management
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Repository
public interface SystemMenuRepository extends JpaRepository<SystemMenu, Integer> {
    
    /**
     * Find visible menu items by parent ID
     * @param pid parent menu ID
     * @return List of menu items
     */
    List<SystemMenu> findByPidAndIsShowTrueOrderBySortAsc(Integer pid);
    
    /**
     * Find all visible menu items
     * @return List of menu items
     */
    List<SystemMenu> findByIsShowTrueOrderBySortAsc();
}
