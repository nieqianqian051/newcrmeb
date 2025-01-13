package com.crmeb.model.system;

import lombok.Data;
import org.hibernate.annotations.SQLDelete;
import org.hibernate.annotations.Where;

import javax.persistence.*;

/**
 * System Role entity representing the eb_system_role table
 * Manages role-based access control
 * 
 * @author Devin
 * @since 2024-01-xx
 */
@Data
@Entity
@Table(name = "eb_system_role")
@SQLDelete(sql = "UPDATE eb_system_role SET is_del = 1 WHERE id = ?")
@Where(clause = "is_del = 0")
public class SystemRole {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "role_name", length = 32)
    private String roleName;

    @Column(columnDefinition = "TEXT")
    private String rules;

    private Boolean status;

    @Column(name = "is_del")
    private Boolean isDel = false;
}
