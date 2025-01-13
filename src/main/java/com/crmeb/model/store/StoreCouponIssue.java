package com.crmeb.model.store;

import lombok.Data;
import org.hibernate.annotations.SQLDelete;
import org.hibernate.annotations.Where;

import javax.persistence.*;
import java.time.LocalDateTime;

/**
 * Coupon Distribution entity representing the eb_store_coupon_issue table
 * Manages coupon issuance and distribution
 * 
 * @author Devin
 * @since 2024-01-xx
 */
@Data
@Entity
@Table(name = "eb_store_coupon_issue")
@SQLDelete(sql = "UPDATE eb_store_coupon_issue SET is_del = 1 WHERE id = ?")
@Where(clause = "is_del = 0")
public class StoreCouponIssue {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(length = 64)
    private String cname;

    private Boolean type;

    private Boolean status;

    @Column(name = "is_del")
    private Boolean isDel = false;

    @Column(name = "create_time")
    private LocalDateTime createTime;

    @Column(name = "update_time")
    private LocalDateTime updateTime;
}
