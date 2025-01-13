package com.crmeb.repository.store;

import com.crmeb.model.store.StoreProduct;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repository interface for StoreProduct entity
 * Provides database operations for product management
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Repository
public interface StoreProductRepository extends JpaRepository<StoreProduct, Integer> {
    
    /**
     * Find products by keyword
     * @param keyword the keyword to search for
     * @param pageable pagination information
     * @return Page of products
     */
    Page<StoreProduct> findByKeywordContaining(String keyword, Pageable pageable);
    
    /**
     * Find active products with stock
     * @return List of available products
     */
    List<StoreProduct> findByIsShowTrueAndStockGreaterThan(Integer minStock);
    
    /**
     * Find products by multiple keywords
     * @param keywords list of keywords
     * @return List of matching products
     */
    @Query("SELECT p FROM StoreProduct p WHERE p.isShow = true AND " +
           "(p.productName LIKE %:keyword% OR p.keyword LIKE %:keyword%)")
    List<StoreProduct> searchByKeywords(String keyword);
}
