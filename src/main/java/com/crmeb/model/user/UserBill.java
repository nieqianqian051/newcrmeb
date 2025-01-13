package com.crmeb.model.user;

import lombok.Data;
import org.hibernate.annotations.SQLDelete;
import org.hibernate.annotations.Where;

import javax.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * User Bill entity representing the eb_user_bill table
 * Manages user transaction records
 * 
 * @author Devin
 * @since 2024-01-xx
 */
@Data
@Entity
@Table(name = "eb_user_bill")
public class UserBill {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "uid")
    private User user;

    @Column(name = "link_id", length = 32)
    private String linkId;

    private Boolean pm;

    @Column(length = 64)
    private String title;

    @Column(precision = 8, scale = 2)
    private BigDecimal number;

    @Column(precision = 8, scale = 2)
    private BigDecimal balance;

    @Column(length = 512)
    private String mark;

    @Column(name = "create_time")
    private LocalDateTime createTime;

    private Boolean status;
}
