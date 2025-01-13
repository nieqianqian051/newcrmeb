package com.crmeb.model.store;

import lombok.Data;
import org.hibernate.annotations.SQLDelete;
import org.hibernate.annotations.Where;

import javax.persistence.*;
import java.math.BigDecimal;

/**
 * Store Combination entity representing the eb_store_combination table
 * Manages group purchase activities
 * 
 * @author Devin
 * @since 2024-01-xx
 */
@Data
@Entity
@Table(name = "eb_store_combination")
@SQLDelete(sql = "UPDATE eb_store_combination SET is_del = 1 WHERE id = ?")
@Where(clause = "is_del = 0")
public class StoreCombination {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "product_id")
    private StoreProduct product;

    private Integer people;

    @Column(precision = 10, scale = 2)
    private BigDecimal price;

    private Boolean status;

    @Column(name = "is_del")
    private Boolean isDel = false;
}
