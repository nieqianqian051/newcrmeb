package com.crmeb.repository.user;

import com.crmeb.model.user.User;
import com.crmeb.model.user.UserLevel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * Repository interface for UserLevel entity
 * Provides database operations for user level management
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Repository
public interface UserLevelRepository extends JpaRepository<UserLevel, Integer> {
    
    /**
     * Find active level by user
     * @param user the user
     * @return Optional containing user level if found
     */
    Optional<UserLevel> findByUserAndStatusTrue(User user);
    
    /**
     * Find level by user and level ID
     * @param user the user
     * @param levelId the level ID
     * @return Optional containing user level if found
     */
    Optional<UserLevel> findByUserAndLevelId(User user, Integer levelId);
}
