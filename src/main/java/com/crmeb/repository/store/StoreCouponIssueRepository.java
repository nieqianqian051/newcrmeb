package com.crmeb.repository.store;

import com.crmeb.model.store.StoreCouponIssue;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repository interface for StoreCouponIssue entity
 * Provides database operations for coupon management
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Repository
public interface StoreCouponIssueRepository extends JpaRepository<StoreCouponIssue, Integer> {
    
    /**
     * Find active coupons
     * @return List of active coupons
     */
    List<StoreCouponIssue> findByStatusTrueAndIsDelFalse();
    
    /**
     * Find coupons by type
     * @param type coupon type
     * @return List of coupons
     */
    List<StoreCouponIssue> findByTypeAndStatusTrue(Boolean type);
}
