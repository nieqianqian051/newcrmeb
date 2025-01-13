package com.crmeb.model.store;

import com.crmeb.model.user.User;
import lombok.Data;
import org.hibernate.annotations.SQLDelete;
import org.hibernate.annotations.Where;

import javax.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * Store Order entity representing the eb_store_order table
 * Handles order management and tracking
 * 
 * @author Devin
 * @since 2024-01-xx
 */
@Data
@Entity
@Table(name = "eb_store_order")
@SQLDelete(sql = "UPDATE eb_store_order SET is_del = 1 WHERE id = ?")
@Where(clause = "is_del = 0")
public class StoreOrder {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "order_id", length = 32)
    private String orderId;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "uid")
    private User user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "product_id")
    private StoreProduct product;

    @Column(name = "total_num")
    private Integer totalNum;

    @Column(name = "total_price", precision = 8, scale = 2)
    private BigDecimal totalPrice;

    private Boolean paid;

    @Column(name = "pay_time")
    private LocalDateTime payTime;

    private Boolean status;

    @Column(name = "refund_status")
    private Boolean refundStatus;

    @Column(name = "create_time")
    private LocalDateTime createTime;

    @Column(name = "update_time")
    private LocalDateTime updateTime;

    @Column(name = "is_del")
    private Boolean isDel = false;
}
