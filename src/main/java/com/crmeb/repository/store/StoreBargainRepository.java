package com.crmeb.repository.store;

import com.crmeb.model.store.StoreBargain;
import com.crmeb.model.store.StoreProduct;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repository interface for StoreBargain entity
 * Provides database operations for bargain activities
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Repository
public interface StoreBargainRepository extends JpaRepository<StoreBargain, Integer> {
    
    /**
     * Find active bargains for a product
     * @param product the product
     * @return List of active bargains
     */
    List<StoreBargain> findByProductAndStatusTrueAndIsDelFalse(StoreProduct product);
    
    /**
     * Find all active bargains
     * @return List of active bargains
     */
    List<StoreBargain> findByStatusTrueAndIsDelFalse();
}
