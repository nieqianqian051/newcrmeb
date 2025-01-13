package com.crmeb.model.user;

import lombok.Data;
import org.hibernate.annotations.SQLDelete;
import org.hibernate.annotations.Where;

import javax.persistence.*;

/**
 * User Address entity representing the eb_user_address table
 * Manages delivery addresses for users
 * 
 * @author Devin
 * @since 2024-01-xx
 */
@Data
@Entity
@Table(name = "eb_user_address")
@SQLDelete(sql = "UPDATE eb_user_address SET is_del = 1 WHERE id = ?")
@Where(clause = "is_del = 0")
public class UserAddress {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "uid")
    private User user;

    @Column(name = "real_name", length = 32)
    private String realName;

    @Column(length = 16)
    private String phone;

    @Column(length = 64)
    private String province;

    @Column(length = 64)
    private String city;

    @Column(length = 64)
    private String district;

    @Column(length = 256)
    private String detail;

    @Column(name = "is_default")
    private Boolean isDefault;
}
