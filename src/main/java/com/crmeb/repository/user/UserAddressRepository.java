package com.crmeb.repository.user;

import com.crmeb.model.user.User;
import com.crmeb.model.user.UserAddress;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * Repository interface for UserAddress entity
 * Provides database operations for delivery address management
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Repository
public interface UserAddressRepository extends JpaRepository<UserAddress, Integer> {
    
    /**
     * Find addresses by user
     * @param user the user
     * @return List of addresses
     */
    List<UserAddress> findByUser(User user);
    
    /**
     * Find default address for user
     * @param user the user
     * @return Optional containing default address if found
     */
    Optional<UserAddress> findByUserAndIsDefaultTrue(User user);
}
