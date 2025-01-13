package com.crmeb.repository.store;

import com.crmeb.model.store.StoreOrder;
import com.crmeb.model.user.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

/**
 * Repository interface for StoreOrder entity
 * Provides database operations for order management
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Repository
public interface StoreOrderRepository extends JpaRepository<StoreOrder, Integer> {
    
    /**
     * Find orders by user
     * @param user the user whose orders to find
     * @param pageable pagination information
     * @return Page of orders
     */
    Page<StoreOrder> findByUser(User user, Pageable pageable);
    
    /**
     * Find unpaid orders created before specified time
     * @param time the cutoff time
     * @return List of unpaid orders
     */
    List<StoreOrder> findByPaidFalseAndCreateTimeBefore(LocalDateTime time);
    
    /**
     * Find order by order ID
     * @param orderId the order ID to search for
     * @return Optional containing the order if found
     */
    StoreOrder findByOrderId(String orderId);
}
