package com.crmeb.model.store;

import lombok.Data;
import org.hibernate.annotations.SQLDelete;
import org.hibernate.annotations.Where;

import javax.persistence.*;
import java.math.BigDecimal;

/**
 * Store Bargain entity representing the eb_store_bargain table
 * Manages bargain activities and pricing
 * 
 * @author Devin
 * @since 2024-01-xx
 */
@Data
@Entity
@Table(name = "eb_store_bargain")
@SQLDelete(sql = "UPDATE eb_store_bargain SET is_del = 1 WHERE id = ?")
@Where(clause = "is_del = 0")
public class StoreBargain {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "product_id")
    private StoreProduct product;

    @Column(length = 255)
    private String title;

    @Column(precision = 10, scale = 2)
    private BigDecimal price;

    @Column(name = "min_price", precision = 10, scale = 2)
    private BigDecimal minPrice;

    private Boolean status;

    @Column(name = "is_del")
    private Boolean isDel = false;
}
