package com.crmeb.repository.user;

import com.crmeb.model.user.User;
import com.crmeb.model.user.UserBill;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * Repository interface for UserBill entity
 * Provides database operations for transaction records
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Repository
public interface UserBillRepository extends JpaRepository<UserBill, Integer> {
    
    /**
     * Find bills by user with pagination
     * @param user the user
     * @param pageable pagination information
     * @return Page of bills
     */
    Page<UserBill> findByUser(User user, Pageable pageable);
    
    /**
     * Find bills by user and type
     * @param user the user
     * @param pm transaction type
     * @param pageable pagination information
     * @return Page of bills
     */
    Page<UserBill> findByUserAndPm(User user, Boolean pm, Pageable pageable);
}
