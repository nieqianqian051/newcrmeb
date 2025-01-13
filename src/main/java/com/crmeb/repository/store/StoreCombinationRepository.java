package com.crmeb.repository.store;

import com.crmeb.model.store.StoreCombination;
import com.crmeb.model.store.StoreProduct;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repository interface for StoreCombination entity
 * Provides database operations for group purchase activities
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Repository
public interface StoreCombinationRepository extends JpaRepository<StoreCombination, Integer> {
    
    /**
     * Find active combinations for a product
     * @param product the product
     * @return List of active combinations
     */
    List<StoreCombination> findByProductAndStatusTrueAndIsDelFalse(StoreProduct product);
    
    /**
     * Find all active combinations
     * @return List of active combinations
     */
    List<StoreCombination> findByStatusTrueAndIsDelFalse();
}
