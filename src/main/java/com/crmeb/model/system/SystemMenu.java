package com.crmeb.model.system;

import lombok.Data;
import org.hibernate.annotations.SQLDelete;
import org.hibernate.annotations.Where;

import javax.persistence.*;

/**
 * System Menu entity representing the eb_system_menus table
 * Manages system navigation menu structure
 * 
 * @author Devin
 * @since 2024-01-xx
 */
@Data
@Entity
@Table(name = "eb_system_menus")
public class SystemMenu {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private Integer pid;

    @Column(length = 16)
    private String name;

    @Column(length = 16)
    private String icon;

    @Column(length = 128)
    private String url;

    private Integer sort;

    @Column(name = "is_show")
    private Boolean isShow;
}
