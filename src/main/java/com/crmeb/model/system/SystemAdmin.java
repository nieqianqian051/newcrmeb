package com.crmeb.model.system;

import lombok.Data;
import org.hibernate.annotations.SQLDelete;
import org.hibernate.annotations.Where;

import javax.persistence.*;

/**
 * System Administrator entity representing the eb_system_admin table
 * Manages system administrators and their permissions
 * 
 * @author Devin
 * @since 2024-01-xx
 */
@Data
@Entity
@Table(name = "eb_system_admin")
@SQLDelete(sql = "UPDATE eb_system_admin SET is_del = 1 WHERE id = ?")
@Where(clause = "is_del = 0")
public class SystemAdmin {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(length = 32)
    private String account;

    @Column(length = 100)
    private String pwd;

    @Column(name = "real_name", length = 16)
    private String realName;

    @Column(length = 128)
    private String roles;

    @Column(name = "last_ip", length = 16)
    private String lastIp;

    private Boolean status;

    @Column(name = "is_del")
    private Boolean isDel = false;
}
