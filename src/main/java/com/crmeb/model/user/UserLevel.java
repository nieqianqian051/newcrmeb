package com.crmeb.model.user;

import lombok.Data;
import org.hibernate.annotations.SQLDelete;
import org.hibernate.annotations.Where;

import javax.persistence.*;

/**
 * User Level entity representing the eb_user_level table
 * Manages user membership levels and privileges
 * 
 * @author Devin
 * @since 2024-01-xx
 */
@Data
@Entity
@Table(name = "eb_user_level")
public class UserLevel {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "uid")
    private User user;

    @Column(name = "level_id")
    private Integer levelId;

    private Integer grade;

    @Column(name = "valid_time")
    private Integer validTime;

    @Column(name = "is_forever")
    private Boolean isForever;

    private Boolean status;
}
