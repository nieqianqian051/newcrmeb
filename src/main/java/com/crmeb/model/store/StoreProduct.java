package com.crmeb.model.store;

import lombok.Data;
import org.hibernate.annotations.SQLDelete;
import org.hibernate.annotations.Where;

import javax.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * Store Product entity representing the eb_store_product table
 * Manages product information and inventory
 * 
 * @author Devin
 * @since 2024-01-xx
 */
@Data
@Entity
@Table(name = "eb_store_product")
@SQLDelete(sql = "UPDATE eb_store_product SET is_del = 1 WHERE id = ?")
@Where(clause = "is_del = 0")
public class StoreProduct {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "product_name", length = 128)
    private String productName;

    @Column(length = 255)
    private String keyword;

    @Column(name = "bar_code", length = 15)
    private String barCode;

    @Column(precision = 8, scale = 2)
    private BigDecimal price;

    @Column(precision = 8, scale = 2)
    private BigDecimal cost;

    private Integer stock;

    private Integer sales;

    @Column(name = "is_show")
    private Boolean isShow;

    @Column(name = "is_del")
    private Boolean isDel = false;

    @Column(name = "create_time")
    private LocalDateTime createTime;

    @Column(name = "update_time")
    private LocalDateTime updateTime;
}
